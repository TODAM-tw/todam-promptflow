from promptflow import tool

@tool
def input_preprocess_tool(question: str) -> str:
    processed_question = ""

    for i in range(len(question)):
        if question[i:i+2] == "  ":
            processed_question += "\\n"
            i += 1
        else:
            processed_question += question[i]

    return processed_question