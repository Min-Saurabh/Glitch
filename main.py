import json
import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import save_tool

load_dotenv()

class CodeResponse(BaseModel):
    code: str
    language: str
    filename: str | None = None

LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
    "java": ".java",
    "c": ".c",
    "cpp": ".cpp",
    "go": ".go",
    "ruby": ".rb",
    "php": ".php",
    "bash": ".sh",
    "shell": ".sh",
    "html": ".html",
    "css": ".css",
    "json": ".json",
    "xml": ".xml",
    "sql": ".sql",
}

def save_code_to_file(code: str, language: str, filename: str | None = None) -> str:
    ext = LANGUAGE_EXTENSIONS.get(language.lower())
    if not ext:
        raise ValueError(f"Unsupported language: {language}")

    safe_filename = filename or "generated_code"
    full_filename = f"{safe_filename}{ext}"

    with open(full_filename, "w", encoding="utf-8") as f:
        f.write(code)
    
    return f"✅ Code saved to `{full_filename}`"

save_tool.func = save_code_to_file


def get_llm(user_key: str | None = None):
    key = user_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("No Gemini API key found.")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=key)


def get_agent_executor(llm):
    parser = PydanticOutputParser(pydantic_object=CodeResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
    You are an AI developer assistant.

    Your task is to generate clean, complete, and functional code in the correct programming language based on a user's query.

    You must return your answer in **raw JSON** using this exact structure:
    {format_instructions}

    ⚠️ STRICT RULES:
    - Return ONLY the JSON block — no markdown formatting, no explanation, no additional text.
    - Provide the correct language name (e.g., "python", "javascript", "cpp", "html").
    - Use descriptive but concise filenames where applicable (no extension needed).

    📚 EXAMPLES:

    1️⃣
    Query:
    Create a Python script that prints "Hello, World!"

    Response:
    {{
    "code": "print('Hello, World!')",
    "language": "python"
    }}

    2️⃣
    Query:
    Write a JavaScript function that sums an array

    Response:
    {{
    "code": "function sumArray(arr) {{ return arr.reduce((a, b) => a + b, 0); }}",
    "language": "javascript",
    "filename": "sum_array"
    }}

    3️⃣
    Query:
    Generate an HTML page with a red button labeled 'Click Me'

    Response:
    {{
    "code": "<!DOCTYPE html>\\n<html>\\n<head><title>Button Page</title></head>\\n<body>\\n  <button style='background:red; color:white;'>Click Me</button>\\n</body>\\n</html>",
    "language": "html",
    "filename": "button_page"
    }}

    4️⃣
    Query:
    Write a C++ program that adds two numbers from user input

    Response:
    {{
    "code": "#include <iostream>\\nusing namespace std;\\n\\nint main() {{\\n  int a, b;\\n  cout << \\\"Enter two numbers: \\\";\\n  cin >> a >> b;\\n  cout << \\\"Sum: \\\" << (a + b) << endl;\\n  return 0;\\n}}",
    "language": "cpp",
    "filename": "sum_input"
    }}

    5️⃣
    Query:
    Write a shell script that lists all `.txt` files in a folder

    Response:
    {{
    "code": "#!/bin/bash\\nls *.txt",
    "language": "bash",
    "filename": "list_txt_files"
    }}

    🚫 Do not wrap output in triple backticks (```) or markdown formatting.
    ✅ Only return the raw JSON object as described above.
                """,
            ),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=[save_tool])
    return AgentExecutor(agent=agent, tools=[save_tool], verbose=True)





if __name__ == "__main__":
    query = input("Enter your query 😎 : ")
    raw_response = get_agent_executor.invoke({"query": query})

    try:
        output_text = raw_response["output"].strip()

        if output_text.startswith("```json"):
            json_response = output_text.replace("```json", "").replace("```", "").strip()
        else:
            json_response = output_text

        json_data = json.loads(json_response)
        structured_response = CodeResponse(**json_data)

        save_result = save_code_to_file(
            structured_response.code,
            structured_response.language,
            structured_response.filename
        )

        print(save_result)

    except Exception as e:
        print("❌ Error parsing response:", e)
        print("Raw Response:", raw_response)
