import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
from threading import Thread
from wsgiref.simple_server import make_server


async def check(server_path):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=[str(server_path)], env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            async def call(name, **arguments):
                response = await session.call_tool(name, arguments)
                assert not response.isError, (name, response)
                return response.structuredContent or json.loads(response.content[0].text)

            plan = await call('create_plan', data={'name': 'integration'})
            for entity, payload, changed in (
                ('note', {'text': 'integration'}, {'text': 'changed'}),
                ('task', {'plan': plan['id'], 'description': 'integration'}, {'priority': 3}),
                ('deduction', {'house': '12.30'}, {'house': '14.00'}),
            ):
                item = await call('create_' + entity, data=payload)
                pk = item['id']
                assert (await call('get_' + entity, id=pk))['id'] == pk
                updated = await call('update_' + entity, id=pk, data=changed)
                for key, value in changed.items():
                    assert updated[key] == value
                if entity == 'note':
                    await call('set_note_image', id=pk, path=os.environ['NB4444_UPLOAD_ROOT'] + '/test.png')
                    image = await session.call_tool('get_note_image', {'id': pk})
                    assert not image.isError and any(block.type == 'image' for block in image.content)
                    random = await call('get_random_notes_with_images', count=10)
                    assert [note['id'] for note in random['items']] == [pk]
                    await call('remove_note_image', id=pk)
                    assert (await call('get_random_notes_with_images', count=10))['items'] == []
                await call('delete_' + entity, id=pk)
                assert (await session.call_tool('get_' + entity, {'id': pk})).isError
                print(entity + ' CRUD: OK')
            await call('update_plan', id=plan['id'], data={'name': 'changed'})
            await call('delete_plan', id=plan['id'])
            assert (await session.call_tool('get_plan', {'id': plan['id']})).isError
            print('plan CRUD: OK')


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / 'NB4444'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'NB4444.settings'
    from django.conf import settings
    with tempfile.TemporaryDirectory(prefix='nb4444-integration-') as folder:
        settings.DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': folder + '/db.sqlite3'}}
        settings.MEDIA_ROOT = folder + '/media'
        settings.SECRET_KEY = 'integration-check-isolated-secret-key-32-characters'
        settings.SIMPLE_JWT['SIGNING_KEY'] = settings.SECRET_KEY
        import django
        django.setup()
        from django.core.management import call_command
        from django.contrib.auth import get_user_model
        from django.core.wsgi import get_wsgi_application
        from rest_framework_simplejwt.tokens import RefreshToken
        from PIL import Image
        call_command('migrate', verbosity=0)
        user = get_user_model().objects.create_user(username='mcp-integration-owner')
        refresh = RefreshToken.for_user(user)
        os.environ['NB4444_ACCESS_TOKEN'] = str(refresh.access_token)
        os.environ['NB4444_REFRESH_TOKEN'] = str(refresh)
        os.environ['NB4444_UPLOAD_ROOT'] = folder
        Image.new('RGB', (2, 2)).save(folder + '/test.png')
        httpd = make_server('127.0.0.1', 0, get_wsgi_application())
        os.environ['NB4444_API_URL'] = f'http://127.0.0.1:{httpd.server_port}'
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            asyncio.run(check(root / 'mcp_server/server.py'))
        finally:
            httpd.shutdown()
            thread.join()
            httpd.server_close()
            from django.db import connections
            connections.close_all()


if __name__ == '__main__':
    main()
