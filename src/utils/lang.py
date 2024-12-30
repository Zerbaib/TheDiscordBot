from src.data.var import folders

def get_language_file(serverLanguage):
    """
    Get the language file depending on the server language

    Args:
        serverLanguage (str): server language

    Returns:
        str: language file path
    """
    return f"{folders['lang']}{serverLanguage.upper()}/lang.json"

