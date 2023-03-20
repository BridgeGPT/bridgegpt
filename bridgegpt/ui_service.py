import asyncio
from _queue import Empty
from queue import Queue

from .ui import Window
from .vo_service import VOService


class UIService:
    def __init__(self, vo_service: VOService):
        self.vo_service = vo_service
        self.healthy = False
        self.loop = asyncio.get_event_loop()
        self._setup_gui()
        self.messages_queue = Queue()

    def _setup_gui(self):
        gui = Window(self.loop, self)
        self.vo_service.set_gptbridge_print(self.add_system_message)
        self.vo_service.set_dialog_print(self.add_message)
        self.gui = gui

    async def exec(self):
        asyncio.create_task(self._initialize_bridgegpt())
        while True:
            try:
                msg = self.messages_queue.get_nowait()
            except Empty:
                msg = None
            if msg and msg['dest'] == 'chat':
                self.gui.display_message(f'{msg["data"]}', from_input=msg["from_input"])
            if msg and msg['dest'] == 'system':
                self.gui.display_system_message(f'{msg["data"]}')
            self.gui.root.update()
            await asyncio.sleep(.01)

    def add_message(self, message, from_input=False):
        self.messages_queue.put({'data': message, 'from_input': from_input, 'dest': 'chat'})

    def add_system_message(self, message, from_input=False):
        self.messages_queue.put({'data': message, 'from_input': from_input, 'dest': 'system'})

    def send_message(self, event=None):
        message = self.gui.input_field.get()
        self.add_message(f'User> {message}', from_input=True)
        asyncio.create_task(self._on_send_message(message))

    async def _on_send_message(self, message):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.vo_service.handle_input, message)
        self.add_message(f'ChatGPT> {response}')

    async def _initialize_bridgegpt(self):
        await self.vo_service.initialize()
