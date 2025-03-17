<<<<<<< HEAD
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # Use the appropriate Gemini model
response = llm.invoke("Hello, how are you?")
print(response)
=======
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # Use the appropriate Gemini model
response = llm.invoke("Hello, how are you?")
print(response)
>>>>>>> 18eeab31 (Initializes the directory)
