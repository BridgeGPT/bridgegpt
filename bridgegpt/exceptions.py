import typing


class BridgeGPTException(BaseException):
    def __init__(self, *a, message: typing.Optional[str] = None):
        super().__init__(*a)
        self.message = message


class UnexpectedResponseException(BridgeGPTException):
    ...
