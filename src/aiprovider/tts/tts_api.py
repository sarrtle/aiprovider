"""TTS api."""

from collections.abc import AsyncGenerator


from aiprovider.tts.schemas.tts_normal_response import TTSNormalResponse
from aiprovider.utils.base_api import BaseApi
from aiprovider.utils.common import (
    convert_file_to_base64,
    get_deepinfra_browser_headers,
)


class TTSApi(BaseApi):
    """TTS api."""

    def __init__(self):
        """Initialize TTSApi."""
        super().__init__()

    async def send_tts(
        self, text: str, model: str, voice_name: str
    ) -> TTSNormalResponse:
        """Send tts."""
        # construct payload
        payload: dict[str, object] = {}
        if model == "canopylabs/orpheus-3b-0.1-ft":
            payload = {"input": text}
        else:
            payload = {"text": text}

        if model == "hexgrad/Kokoro-82M":
            payload["output_format"] = "opus"
        else:
            payload["response_format"] = "opus"

        # select voice
        if voice_name == "canopylabs/orpheus-3b-0.1-ft":
            payload["voice"] = voice_name
        elif voice_name == "hexgrad/Kokoro-82M":
            payload["preset_voice"] = [voice_name]

        # model as url
        url = "https://api.deepinfra.com/v1/inference/" + model

        headers: dict[str, str] = {"Connection": "keep-alive"}

        # if simulating browser
        if self._is_browser:
            # set httpx header
            headers.update(get_deepinfra_browser_headers())

        # with api keyss
        else:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }

        # send request
        response = await self._client.post(url, json=payload, headers=headers)

        tts_response = TTSNormalResponse.model_validate(response.json())

        return tts_response

    async def send_tts_stream(self, text: str) -> AsyncGenerator[bytes]:
        """Send tts as stream."""
        print(text)
        raise NotImplementedError

    async def send_tts_with_clone_audio(
        self, text: str, model: str, audio_to_clone: str, audio_transcript: str
    ) -> TTSNormalResponse:
        """Send tts with clone audio."""
        # construct payload
        payload: dict[str, object] = {}
        payload["max_audio_length_ms"] = 60000
        payload["response_format"] = "opus"
        payload["speaker_audio"] = await convert_file_to_base64(audio_to_clone)
        payload["speaker_transcript"] = audio_transcript
        payload["text"] = text

        url = "https://api.deepinfra.com/v1/inference/" + model

        headers: dict[str, str] = {"Connection": "keep-alive"}

        # if simulating browser
        if self._is_browser:
            # set httpx header
            headers.update(get_deepinfra_browser_headers())

        # with api keyss
        else:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }

        # send request
        response = await self._client.post(
            url, json=payload, headers=headers, timeout=300
        )

        tts_response = TTSNormalResponse.model_validate(response.json())

        return tts_response
