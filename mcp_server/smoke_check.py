"""Read-only protocol smoke check; run in the configured MCP container."""
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command=sys.executable, args=['/app/server.py'], env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert 'get_random_notes_with_images' in {tool.name for tool in tools.tools}
            assert all(tool.description for tool in tools.tools)
            for name, args in [('get_current_user', {}), ('list_sections', {}),
                               ('list_notes', {'page_size': 1, 'has_image': True}),
                               ('list_plans', {'page_size': 1}),
                               ('list_tasks', {'page_size': 1}),
                               ('list_deductions', {'page_size': 1}),
                               ('get_random_notes_with_images', {'count': 10})]:
                result = await session.call_tool(name, args)
                assert not result.isError, (name, result)
                print(name + ': OK')
                if name == 'get_random_notes_with_images':
                    import json
                    payload = result.structuredContent
                    if payload is None:
                        payload = json.loads(result.content[0].text)
                    items = payload['items']
                    print('random notes count:', len(items))
                    if items:
                        image = await session.call_tool('get_note_image', {'id': items[0]['id']})
                        assert not image.isError, image
                        assert any(block.type == 'image' for block in image.content)
                        print('get_note_image: OK')
            assert (await session.list_resources()).resources
            assert (await session.list_prompts()).prompts
            print('resources/prompts: OK')


if __name__ == '__main__':
    asyncio.run(main())
