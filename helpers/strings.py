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
