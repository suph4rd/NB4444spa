from pathlib import Path

import httpx
from mcp.server.fastmcp import Image


from ..api_client import NB4444ApiClient
from ..settings import ServerSettings


MAX_IMAGE_SIZE = 10 * 1024 * 1024


class NoteImageService:

    def __init__(self, settings: ServerSettings, api_client: NB4444ApiClient):
        self.settings = settings
        self.api_client = api_client

    def set_note_image(self, id: int, path: str) -> dict:
        from PIL import Image as PILImage
        upload_root = self.settings.upload_root
        if not upload_root:
            raise ValueError('validation_error: NB4444_UPLOAD_ROOT не настроен')
        try:
            root = Path(upload_root).resolve()
            source = Path(path).resolve()
            if (not source.is_relative_to(root) or not source.is_file()
                    or source.stat().st_size > MAX_IMAGE_SIZE):
                raise ValueError('validation_error: недопустимый файл')
            with PILImage.open(source) as img:
                if img.format not in ('JPEG', 'PNG', 'WEBP'):
                    raise ValueError('validation_error: формат изображения')
                img.verify()
            with source.open('rb') as file:
                return self.api_client.read_json(self.api_client.request('PATCH', f'/api/v1/note/{id}/',
                                         files={'image': (source.name, file)}))
        except (OSError, SyntaxError, PILImage.DecompressionBombError) as error:
            raise ValueError('validation_error: файл недоступен или повреждён') from error

    def remove_note_image(self, id: int) -> dict:
        return self.api_client.read_json(self.api_client.request('PATCH', f'/api/v1/note/{id}/', json={'image': None}))

    def get_note_image(self, id: int) -> Image:
        from io import BytesIO
        from PIL import Image as PILImage
        response = self.api_client.request('GET', f'/api/v1/note/{id}/image/', stream=True)
        try:
            data = bytearray()
            for chunk in response.iter_bytes(chunk_size=65536):
                if len(data) + len(chunk) > MAX_IMAGE_SIZE:
                    raise ValueError('validation_error: слишком большое изображение')
                data.extend(chunk)
            try:
                with PILImage.open(BytesIO(data)) as img:
                    image_format = img.format
                    if image_format not in ('JPEG', 'PNG', 'WEBP'):
                        raise ValueError('validation_error: формат изображения')
                    img.verify()
            except (OSError, SyntaxError, PILImage.DecompressionBombError) as error:
                raise ValueError('validation_error: повреждённое изображение') from error
            return Image(data=bytes(data), format=image_format.lower())
        except httpx.HTTPError:
            raise ValueError('api_unavailable: ошибка скачивания изображения') from None
        finally:
            response.close()


def register_images(mcp, service):
    mcp.tool(description='Загрузить JPEG/PNG/WebP до 10 МиБ из NB4444_UPLOAD_ROOT в заметку.')(service.set_note_image)
    mcp.tool(description='Удалить связь заметки с фотографией.')(service.remove_note_image)
    mcp.tool(description='Получить фотографию доступной заметки, максимум 10 МиБ.')(service.get_note_image)
