import logging

from nb4444_mcp.api_client import NB4444ApiClient
from nb4444_mcp.application import create_server
from nb4444_mcp.settings import ServerSettings


def main():
    logging.basicConfig()
    settings = ServerSettings.from_environment()
    api_client = NB4444ApiClient(settings)
    try:
        create_server(settings, api_client).run(transport='stdio')
    finally:
        api_client.close()


if __name__ == '__main__':
    main()
