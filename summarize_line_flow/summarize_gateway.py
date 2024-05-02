from promptflow.tools.aoai import tool

@tool
def summarize_gateway(
    is_english: str, is_chinese: str
) -> str:
    if is_chinese is not None:
        return is_chinese
    
    return is_english