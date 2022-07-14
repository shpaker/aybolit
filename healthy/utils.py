from typing import Optional


def get_error_message_from_assert(
    exc: AssertionError
) -> Optional[str]:
    message = exc.args[0]
    if '\n' not in message:
        return None
    return message.split('\n')[0]
