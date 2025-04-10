"""Common utils."""

import base64
import mimetypes
import aiofiles
from httpx import Response


def get_deepinfra_browser_headers():
    """Get browser headers."""
    return {
        "Content-Type": "application/json",
        "Host": "api.deepinfra.com",
        "Origin": "https://deepinfra.com",
        "Pragma": "no-cache",
        "Referer": "https://deepinfra.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36",
        "Priority": "u=0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Deepinfra-Source": "model-embed",
    }


async def save_tts_to_file(base64_audio: str, file_path: str):
    """Convert base64 audio to file."""
    base64_data = base64_audio.split(",")[1]
    async with aiofiles.open(file_path, "wb") as f:
        _ = await f.write(base64.b64decode(base64_data))


async def convert_file_to_base64(file_path: str) -> str:
    """Convert audio to base64."""
    mimetype, _ = mimetypes.guess_type(file_path)
    if not mimetype:
        raise ValueError(f"Could not determine mimetype for {file_path}")

    async with aiofiles.open(file_path, "rb") as f:
        audio_bytes = await f.read()

    base64_audio = (
        f"data:{mimetype};base64,{base64.b64encode(audio_bytes).decode('utf-8')}"
    )

    return base64_audio


async def convert_response_to_base64(response: Response):
    """Convert audio to base64."""
    mimetype: str | None = response.headers.get("Content-Type", None)

    if not mimetype:
        raise ValueError(f"Could not determine mimetype for {response.url}")

    response_bytes = response.read()

    base64_audio = (
        f"data:{mimetype};base64,{base64.b64encode(response_bytes).decode('utf-8')}"
    )

    return base64_audio
