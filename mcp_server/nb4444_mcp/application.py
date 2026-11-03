from mcp.server.fastmcp import FastMCP

from .api_client import NB4444ApiClient
from .prompts import register_prompts
from .resources import register_resources
from .settings import ServerSettings
from .tools.crud import register_crud
from .tools.images import NoteImageService, register_images
from .tools.queries import register_queries, register_random_query


def create_server(settings: ServerSettings, api_client: NB4444ApiClient) -> FastMCP:
    mcp = FastMCP('NB4444')
    register_crud(mcp, api_client)
    register_queries(mcp, api_client)
    register_images(mcp, NoteImageService(settings, api_client))
    register_random_query(mcp, api_client)
    register_resources(mcp)
    register_prompts(mcp)
    return mcp
