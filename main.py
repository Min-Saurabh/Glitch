import json
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_Tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    response: str
    sources: list[str]
    tools_Used: list[str]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_Tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("How can I help you? ")
raw_Response = agent_executor.invoke({"query": query})

try:
    output_text = raw_Response["output"].strip()

    print("Raw Output:", output_text)

    if output_text.startswith("```json"):
        json_response = output_text.replace("```json", "").replace("```", "").strip()
    else:
        json_response = output_text

    json_data = json.loads(json_response)
    structured_response = ResearchResponse(**json_data)

    print("Structured Response:", structured_response)

    print("Tools Used:", structured_response.tools_Used)

    if "save_text_to_file" in structured_response.tools_Used:
        print("Saving to file...")
        save_result = save_tool.func(structured_response.response)
        print(save_result)
    else:
        print("Save tool was not invoked.")

except Exception as e:
    print("Error parsing response:", e, "Raw Response - ", raw_Response)