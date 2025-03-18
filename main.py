import json
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

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  
parser = PydanticOutputParser(pydantic_object=CodeResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an AI code generator. Write the code based on the provided query and save it to a file automatically.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),  #Placeholder for agent_scratchpad
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[save_tool]
)

agent_executor = AgentExecutor(agent=agent, tools=[save_tool], verbose=True)

query = input("Enter your query: ")
raw_Response = agent_executor.invoke({"query": query})

try:
    output_text = raw_Response["output"].strip()

    if output_text.startswith("```json"):
        json_response = output_text.replace("```json", "").replace("```", "").strip()
    else:
        json_response = output_text

    json_data = json.loads(json_response)
    structured_response = CodeResponse(**json_data)

    # Automatically save the generated code
    save_result = save_tool.func(structured_response.code)
    print(save_result)

except Exception as e:
    print("Error parsing response:", e, "Raw Response - ", raw_Response)