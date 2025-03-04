import traceback


def normalize_string(text: str) -> str:
    """
    Normalizes a string by replacing all symbols and spaces with hyphens.
    Multiple consecutive symbols/spaces will be collapsed into a single hyphen.

    Args:
        text (str): The string to normalize

    Returns:
        str: The normalized string with symbols/spaces replaced by hyphens
    """
    if not text:
        return text

    # Replace all non-alphanumeric characters with hyphens
    import re

    normalized = re.sub(r"[^a-zA-Z0-9]", "-", text)

    # Collapse multiple consecutive hyphens into one
    normalized = re.sub(r"-+", "-", normalized)

    # Remove leading/trailing hyphens
    normalized = normalized.strip("-")

    return normalized


def obfuscate_string(text: str) -> str:
    """
    Obfuscates a string by keeping first 3 and last 3 characters, replacing middle with '***'.
    For strings shorter than 6 characters, keeps first character and adds '***'.

    Args:
        text (str): The string to obfuscate

    Returns:
        str: The obfuscated string
    """
    if not text:
        return text
    if len(text) < 6:
        return f"{text[0]}***"

    return f"{text[:3]}***{text[-3:]}"


def parse_boolean(value: str) -> bool:
    """Parse a boolean value from a string"""
    if value.lower() in ["true", "1", "yes", "on", "enabled", "enable", "t", "y"]:
        return True
    return False


def get_error_from_exception(message: str, e: Exception) -> dict:
    """Get the error from an exception"""
    return {
        "error_message": f"{message}: {str(e)}",
        "error_type": type(e).__name__,
        "traceback": traceback.format_exc(),
    }


def get_context_variable(
    key: str, session_context: dict, context_variables: dict
) -> str | None:
    """Get the value of a context variable from the session context"""
    if session_context:
        if key in session_context:
            return session_context[key]
    if context_variables:
        if key in context_variables:
            return context_variables[key]
    return None
