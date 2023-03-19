from dataclasses import dataclass
from enum import Enum


class ChatRole(Enum):
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'


@dataclass
class ChatMessage:
    role: ChatRole
    content: str

    def serialize(self):
        return {
            "role": self.role.value,
            "content": self.content
        }
