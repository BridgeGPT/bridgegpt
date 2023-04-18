import asyncio
import json
import logging
from asyncio import CancelledError

from bridgegpt.data_types import ChatMessage, ChatRole
from bridgegpt.exceptions import UnexpectedResponseException
from bridgegpt.openai_service import OpenAIService
from bridgegpt.prompts_service import PromptsService
from bridgegpt.system_service import SystemService


logger = logging.getLogger('bridge.vo_service')


class VOService:
    def __init__(
        self,
        system_service: SystemService,
        openai_service: OpenAIService,
        prompts_service: PromptsService,
    ):
        self.system_service = system_service
        self.openai_service = openai_service
        self.prompts_service = prompts_service
        self.current_context = [self.prompts_service.get_base_prompt()]
        self.gptbridge_print_fn = lambda x: None
        self.dialog_print_fn = None

    @classmethod
    def instance(cls):
        openai_service = OpenAIService()
        system_service = SystemService()
        prompts_service = PromptsService()
        return cls(
            system_service=system_service,
            openai_service=openai_service,
            prompts_service=prompts_service
        )

    def set_gptbridge_print(self, fn: callable):
        self.gptbridge_print_fn = fn

    def set_dialog_print(self, fn: callable):
        self.dialog_print_fn = fn

    async def initialize(self):
        msgs = self.current_context + [
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content="Understood, tell me a command"
            ),
            ChatMessage(
                role=ChatRole.USER,
                content="tell me the kernel version"
            ),
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content='{"id": 1, "action": "uname -r", from: "ChatGPT"}'
            ),
            ChatMessage(
                role=ChatRole.USER,
                content='{"id": 1, "response": "5.19.0-38-generic"", "from": "BridgeGPT"}'
            ),
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content="The current kernel version is 5.19.0-38-generic"
            ),
            self.prompts_service.get_self_test_prompt()
        ]
        self.gptbridge_print_fn({"id": 0, "from": "BridgeGPT", "response": "Starting BridgeGPT\n"})
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, self.openai_service.generate_response, msgs)
        valid_json = self.system_service.is_valid_json(resp)
        if not valid_json:
            logger.exception('Failed response:\n\n\n%s\n\n\n, expected JSON', resp)
            raise UnexpectedResponseException(message=resp)
        msgs.append(ChatMessage(role=ChatRole.ASSISTANT, content=resp))
        outcome = self.system_service.execute_command(command_id=valid_json['id'], command=valid_json['action'])
        msgs.append(ChatMessage(role=ChatRole.SYSTEM, content=json.dumps(outcome)))
        resp = await loop.run_in_executor(None, self.openai_service.generate_response, msgs)
        self.gptbridge_print_fn({"id": 0, "from": "ChatGPT", "response": resp})

    def handle_input(self, user_input: str):
        self.current_context.append(ChatMessage(role=ChatRole.SYSTEM, content=user_input))
        resp = self.openai_service.generate_response(self.current_context)
        while self.system_service.is_valid_json(resp):
            valid_json = self.system_service.is_valid_json(resp)
            self.gptbridge_print_fn(valid_json)
            self.current_context.append(ChatMessage(role=ChatRole.ASSISTANT, content=resp))
            outcome = self.system_service.execute_command(command_id=valid_json['id'], command=valid_json['action'])
            self.gptbridge_print_fn(outcome)
            self.current_context.append(ChatMessage(role=ChatRole.USER, content=json.dumps(outcome)))
            resp = self.openai_service.generate_response(self.current_context, temperature=1)
        return resp
