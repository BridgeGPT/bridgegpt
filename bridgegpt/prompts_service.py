import os

from bridgegpt.data_types import ChatMessage, ChatRole


class PromptsService:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))

    def _load_prompt(self, file_name: str):
        with open(os.path.join(self.script_dir, f"prompts/{file_name}.txt"), "r") as f:
            return f.read().strip()

    def get_base_prompt(self) -> ChatMessage:
        return ChatMessage(
            role=ChatRole.SYSTEM,
            content=self._load_prompt('base_prompt')
        )

    def get_self_test_prompt(self):
        return ChatMessage(
            role=ChatRole.USER,
            content=self._load_prompt('self_test_message')
        )
