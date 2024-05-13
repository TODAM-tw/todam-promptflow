from promptflow.tools.aoai import tool

@tool
def detect_language(line_log: str) -> str:
    chinese_range = ('\u4e00', '\u9fff')
    has_chinese = any(chinese_range[0] <= char <= chinese_range[1] for char in line_log)

    if has_chinese:
        return 'Chinese'
    
    return line_log