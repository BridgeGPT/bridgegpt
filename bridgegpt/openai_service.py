import json
import logging
import typing

import openai
import os

from bridgegpt.data_types import ChatMessage


logger = logging.getLogger('bridge.openai_service')
logger.setLevel(logging.DEBUG)


class OpenAIService:
    def __init__(self):
        self.model_id = "gpt-3.5-turbo"
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def generate_response(self, messages: typing.List[ChatMessage], max_tokens=2048, temperature=0.9):
        serialized = [x.serialize() for x in messages]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            presence_penalty=0,
            frequency_penalty=0,
            messages=serialized
        )
        msg = response.choices[0].message
        ai_response = msg.content.strip()
        logger.debug(
            'generate_response - messages:\n%s\n\nresponse:\n%s\n',
            json.dumps(serialized, indent=2), ai_response
        )
        return ai_response
