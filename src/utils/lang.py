from src.data.var import folders
import json, os

def get_language_file(serverLanguage):
    """
    Get the language file depending on the server language

    Args:
        serverLanguage (str): server language

    Returns:
        dict: language file content
    """

    if not serverLanguage:
        serverLanguage = "EN"

    language_file_path = f"{folders['lang']}{str(serverLanguage).upper()}/lang.json"

    if not os.path.exists(language_file_path):
        language_file_path = f"{folders['lang']}EN/lang.json"

    with open(language_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

