from promptflow.tools.aoai import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(
    summarize_contents_output: str, ask_more_information_output: str
) -> str:
    if summarize_contents_output is not None:
        return summarize_contents_output

    return ask_more_information_output
