from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

class Research_Response(BaseModel):
    topic: str
    response: str
    sources: list[str]
    tools_Used: list[str]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  
parser = PydanticOutputParser(pydantic_object=Research_Response)

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

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)

agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)

raw_Response = agent_executor.invoke({"query": "What is your name?"})
print(raw_Response)

try:
    structured_response = parser.parse(raw_Response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_Response)