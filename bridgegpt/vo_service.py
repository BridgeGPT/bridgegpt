import logging

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
        prompts_service: PromptsService
    ):
        self.system_service = system_service
        self.openai_service = openai_service
        self.prompts_service = prompts_service
        self.current_context = [self.prompts_service.get_base_prompt()]

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

    def initialize(self):
        msgs = self.current_context + [self.prompts_service.get_self_test_prompt()]
        resp = self.openai_service.generate_response(msgs)
        valid_json = self.system_service.is_valid_json(resp)
        if not valid_json:
            logger.exception('Failed response:\n%s\n, expected JSON', resp)
            raise UnexpectedResponseException(message=resp)
        msgs.append(ChatMessage(role=ChatRole.ASSISTANT, content=resp))
        outcome = self.system_service.execute_command(command_id=valid_json['id'], command=valid_json['action'])
        msgs.append(ChatMessage(role=ChatRole.SYSTEM, content=outcome))
        resp = self.openai_service.generate_response(msgs)
        return resp

    def handle_input(self, user_input: str):
        self.current_context.append(ChatMessage(role=ChatRole.USER, content=user_input))
        resp = self.openai_service.generate_response(self.current_context)
        i = 0
        while self.system_service.is_valid_json(resp):
            valid_json = self.system_service.is_valid_json(resp)
            i += 1
            self.current_context.append(ChatMessage(role=ChatRole.ASSISTANT, content=resp))
            outcome = self.system_service.execute_command(command_id=valid_json['id'], command=valid_json['action'])
            self.current_context.append(ChatMessage(role=ChatRole.SYSTEM, content=outcome))
            resp = self.openai_service.generate_response(self.current_context)
        if not i:
            logger.exception(resp)
            raise UnexpectedResponseException(message=resp)
        return resp
