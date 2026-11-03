import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from PIL import Image
import server


class MCPTests(unittest.TestCase):
    def setUp(self):
        self.original = server.client
        self.calls = []
        self.responses = []

        def handle(request):
            self.calls.append(request)
            value = self.responses.pop(0)
            if isinstance(value, Exception):
                raise value
            return value

        server.client = httpx.Client(transport=httpx.MockTransport(handle))

    def tearDown(self):
        server.client.close()
        server.client = self.original

    def tool(self, name, **kwargs):
        return server.mcp._tool_manager.get_tool(name).fn(**kwargs)

    def test_write_schema_and_unknown_fields(self):
        tool = server.mcp._tool_manager.get_tool('create_task')
        schema = tool.parameters['properties']['data']
        self.assertIn('plan', schema['properties'])
        self.assertFalse(schema['additionalProperties'])
        with self.assertRaisesRegex(ValueError, 'неизвестные поля'):
            self.tool('create_note', data={'user': 999})
        self.assertEqual(self.calls, [])

    def test_special_tools_invalid_json(self):
        for name, kwargs in (
            ('get_current_user', {}), ('list_sections', {}),
            ('get_latest_deductions', {}), ('remove_note_image', {'id': 1}),
        ):
            self.responses = [httpx.Response(200, text='bad')]
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'api_unavailable'):
                self.tool(name, **kwargs)

    def test_refresh_service_failure(self):
        self.responses = [httpx.Response(401), httpx.Response(503)]
        with self.assertRaisesRegex(ValueError, 'api_unavailable'):
            self.tool('get_plan', id=1)

    def test_crud_http_contract(self):
        for entity, endpoint in (('note', 'note'), ('plan', 'plan'),
                                 ('task', 'task'), ('deduction', 'default-deduction')):
            with self.subTest(entity=entity):
                self.responses = [httpx.Response(201, json={'id': 7}),
                                  httpx.Response(200, json={'id': 7}),
                                  httpx.Response(200, json={'id': 7}), httpx.Response(204)]
                self.assertEqual(self.tool('create_' + entity, data={})['id'], 7)
                self.tool('get_' + entity, id=7)
                self.tool('update_' + entity, id=7, data={})
                self.assertTrue(self.tool('delete_' + entity, id=7)['deleted'])
                self.assertEqual([call.method for call in self.calls[-4:]],
                                 ['POST', 'GET', 'PATCH', 'DELETE'])
                self.assertEqual(self.calls[-1].url.path, f'/api/v1/{endpoint}/7/')

    def test_all_tools_have_descriptions(self):
        self.assertTrue(all(t.description for t in server.mcp._tool_manager.list_tools()))

    def test_pagination(self):
        self.responses = [httpx.Response(200, json=[{'id': 3}, {'id': 4}, {'id': 5}])]
        result = self.tool('list_notes', offset=2, page_size=2, has_image=True)
        self.assertEqual(result['next_offset'], 4)
        self.assertEqual(len(result['items']), 2)
        self.assertEqual(self.calls[0].url.params['limit'], '5')
        self.assertEqual(self.calls[0].url.params['has_image'], 'true')

    def test_invalid_filters_and_pagination(self):
        for kwargs in ({'page_size': 101}, {'offset': -1}, {'plan': 1}):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, 'validation_error'):
                self.tool('list_notes', **kwargs)
        self.assertEqual(self.calls, [])

    def test_permission_does_not_refresh(self):
        self.responses = [httpx.Response(403, json={'detail': 'Forbidden'})]
        with self.assertRaisesRegex(ValueError, 'permission_denied'):
            self.tool('get_plan', id=1)
        self.assertEqual(len(self.calls), 1)

    def test_refresh_once(self):
        self.responses = [httpx.Response(401), httpx.Response(200, json={'access': 'new'}),
                          httpx.Response(401)]
        with self.assertRaisesRegex(ValueError, 'authentication_required'):
            self.tool('get_plan', id=1)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.calls[-1].headers['authorization'], 'Bearer new')

    def test_bad_refresh_payload(self):
        self.responses = [httpx.Response(401), httpx.Response(200, json={})]
        with self.assertRaisesRegex(ValueError, 'некорректный ответ'):
            self.tool('get_plan', id=1)

    def test_validation_details(self):
        self.responses = [httpx.Response(400, json={'name': ['Required']})]
        with self.assertRaisesRegex(ValueError, 'name'):
            self.tool('create_plan', data={})

    def test_network_write_not_retried(self):
        self.responses = [httpx.ReadTimeout('timeout')]
        with self.assertRaisesRegex(ValueError, 'результат записи'):
            self.tool('create_plan', data={'name': 'x'})
        self.assertEqual(len(self.calls), 1)

    def test_invalid_json_and_shape(self):
        for response in (httpx.Response(200, text='bad'), httpx.Response(200, json={})):
            self.responses = [response]
            with self.assertRaisesRegex(ValueError, 'api_unavailable'):
                self.tool('list_notes')

    def test_random_unique_and_short(self):
        self.responses = [httpx.Response(200, json=[{'id': 1, 'image': 'a'},
                          {'id': 1, 'image': 'a'}, {'id': 2, 'image': 'b'}])]
        self.assertEqual(len(server.get_random_notes_with_images()['items']), 2)

    def test_upload_paths(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, NB4444_UPLOAD_ROOT=folder):
            for path in (folder, folder + '/missing', '/etc/passwd'):
                with self.assertRaisesRegex(ValueError, 'validation_error'):
                    server.set_note_image(1, path)
            bad = Path(folder) / 'bad.png'
            bad.write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError, 'validation_error'):
                server.set_note_image(1, str(bad))

    def test_image_download(self):
        output = io.BytesIO()
        Image.new('RGB', (2, 2)).save(output, format='PNG')
        self.responses = [httpx.Response(200, content=output.getvalue())]
        self.assertIsNotNone(server.get_note_image(1))

    def test_stream_stops_and_closes_at_size_limit(self):
        class Stream(httpx.SyncByteStream):
            chunks = 0
            closed = False

            def __iter__(self):
                for _ in range(100):
                    self.chunks += 1
                    yield b'x' * 65536

            def close(self):
                self.closed = True

        stream = Stream()
        self.responses = [httpx.Response(200, stream=stream)]
        with patch.object(server, 'MAX_IMAGE_SIZE', 65536):
            with self.assertRaisesRegex(ValueError, 'слишком большое'):
                server.get_note_image(1)
        self.assertEqual(stream.chunks, 2)
        self.assertTrue(stream.closed)

    def test_image_size_limit(self):
        self.responses = [httpx.Response(200, content=b'x' * 20)]
        with patch.object(server, 'MAX_IMAGE_SIZE', 10):
            with self.assertRaisesRegex(ValueError, 'слишком большое'):
                server.get_note_image(1)


if __name__ == '__main__':
    unittest.main()
