import tiktoken

def get_information(text: str, model_name: str = "gpt-4o") -> str:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")

    words = len(text.split())
    chars = len(text)
    tokens = len(encoding.encode(text))

    return f"Words:      {words}\nCharacters: {chars}\nTokens:     {tokens}"
