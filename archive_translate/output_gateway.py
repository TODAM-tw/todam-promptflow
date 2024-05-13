from promptflow.tools.aoai import tool

@tool
def output_gateway(
    english_result: str, chinese_result: str
) -> str:
    if chinese_result is not None:
        return chinese_result
    
    return english_result