from typing import Optional


def get_error_message_from_assert(exc: Exception) -> Optional[str]:
    if not exc.args:
        return None
    message = exc.args[0]
    if '\n' not in message:
        return None
    return message.split('\n')[0]
