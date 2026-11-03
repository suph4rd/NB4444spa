"""Contract captured from the original server before the package refactor."""
import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import server
from nb4444_mcp.api_client import NB4444ApiClient
from nb4444_mcp.application import create_server
from nb4444_mcp.settings import ServerSettings


CONTRACT = json.loads((Path(__file__).parent / 'fixtures' / 'mcp_contract.json').read_text())


class ContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_factory_contract(self):
        api_client = NB4444ApiClient(ServerSettings(), httpx.Client(transport=httpx.MockTransport(
            lambda request: self.fail('Registration must not access the API'))))
        self.addCleanup(api_client.close)
        mcp = create_server(ServerSettings(), api_client)
        self.assertEqual([t.model_dump(mode='json') for t in await mcp.list_tools()], CONTRACT['tools'])
        self.assertEqual([r.model_dump(mode='json') for r in await mcp.list_resources()], CONTRACT['resources'])
        self.assertEqual([p.model_dump(mode='json') for p in await mcp.list_prompts()], CONTRACT['prompts'])
        self.assertIn('Заметки:', (await mcp.read_resource('nb4444://guide'))[0].content)

    async def test_stdio_contract_from_arbitrary_directory(self):
        with tempfile.TemporaryDirectory() as cwd:
            params = StdioServerParameters(
                command=sys.executable, args=[str(Path(server.__file__).resolve())], cwd=cwd,
                env={'PATH': os.environ.get('PATH', ''), 'NB4444_API_URL': 'http://127.0.0.1:1'},
            )
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.assertEqual([t.model_dump(mode='json') for t in (await session.list_tools()).tools], CONTRACT['tools'])
                    self.assertEqual([r.model_dump(mode='json') for r in (await session.list_resources()).resources], CONTRACT['resources'])
                    self.assertEqual([p.model_dump(mode='json') for p in (await session.list_prompts()).prompts], CONTRACT['prompts'])
                    prompt = await session.get_prompt('review_plan', {'plan_id': '7'})
                    self.assertEqual(prompt.messages[0].content.text,
                                     'Прочитай план 7 и его задачи, оцени прогресс и предложи следующие действия.')


class DependencyTests(unittest.TestCase):
    def test_clients_refresh_independently(self):
        calls = [[], []]
        def transport(index):
            def handle(request):
                calls[index].append(request)
                if request.url.path == '/auth/jwt/refresh/':
                    self.assertEqual(json.loads(request.content), {'refresh': f'refresh-{index}'})
                    return httpx.Response(200, json={'access': f'new-{index}'})
                if request.headers['authorization'] == f'Bearer old-{index}':
                    return httpx.Response(403, json={'code': 'token_not_valid'})
                return httpx.Response(200, json={'id': index})
            return httpx.MockTransport(handle)
        clients = [NB4444ApiClient(
            ServerSettings(access_token=f'old-{i}', refresh_token=f'refresh-{i}'),
            httpx.Client(transport=transport(i))) for i in range(2)]
        for client in clients:
            self.addCleanup(client.close)
        clients[0].request('GET', '/api/v1/plan/1/')
        self.assertEqual(clients[1].token, 'old-1')
        clients[1].request('GET', '/api/v1/plan/1/')
        clients[0].request('GET', '/api/v1/plan/2/')
        self.assertEqual(clients[0].token, 'new-0')
        self.assertEqual(clients[1].token, 'new-1')
        self.assertEqual([len(items) for items in calls], [4, 3])

    def test_main_closes_client_on_exit_and_error(self):
        for error in (None, RuntimeError('stdio failed')):
            with self.subTest(error=error), patch.object(server, 'NB4444ApiClient') as client, \
                    patch.object(server, 'create_server') as factory:
                factory.return_value.run.side_effect = error
                if error:
                    with self.assertRaises(RuntimeError):
                        server.main()
                else:
                    server.main()
                factory.return_value.run.assert_called_once_with(transport='stdio')
                client.return_value.close.assert_called_once()

    def test_settings_environment_and_defaults(self):
        self.assertEqual(ServerSettings.from_environment({}), ServerSettings())
        settings = ServerSettings.from_environment({
            'NB4444_API_URL': 'http://example.test/', 'NB4444_ACCESS_TOKEN': 'access',
            'NB4444_REFRESH_TOKEN': 'refresh', 'NB4444_HTTP_TIMEOUT': '12.5',
            'NB4444_UPLOAD_ROOT': '/uploads',
        })
        self.assertEqual(settings, ServerSettings('http://example.test', 'access', 'refresh', 12.5, '/uploads'))
        self.assertNotIn('refresh', repr(settings))
