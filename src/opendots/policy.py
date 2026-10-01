"""Small, explicit request-boundary checks for the agent runtime."""


class InputLimitError(ValueError):
    """Raised when a prompt exceeds the configured input limit."""


def validate_input(message: str, max_chars: int) -> None:
    if not message.strip():
        raise ValueError("Message must not be empty")
    if len(message) > max_chars:
        raise InputLimitError(
            f"Message is {len(message)} characters; configured limit is {max_chars}"
        )
