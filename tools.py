from langchain.tools import Tool

def save_to_txt(data: str, filename: str = "generated_code.py"):
    try:
        formatted_text = f"# Generated Code\n\n{data}\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)

        print(f"Code successfully saved to {filename}")
        return f"Code successfully saved to {filename}"
    except Exception as e:
        print(f"Error writing to file: {e}")
        return f"Error writing to file: {e}"

save_tool = Tool(
    name="save_code_to_file",
    func=save_to_txt,
    description="Saves generated code to a Python file.",
)