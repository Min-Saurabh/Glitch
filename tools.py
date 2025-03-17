from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# Function to Save Data to a File
def save_to_txt(data: str, filename: str = "research_output.txt"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)

        print(f"Data successfully saved to {filename}")  # Debugging print
        return f"Data successfully saved to {filename}"
    except Exception as e:
        print(f"Error writing to file: {e}")
        return f"Error writing to file: {e}"

# Save Tool
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

# Search Tool
search = DuckDuckGoSearchRun()
search_Tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information.",
)

# Wikipedia Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_search = WikipediaQueryRun(api_wrapper=api_wrapper)
wiki_tool = Tool(
    name="wikipedia",
    func=wiki_search.run,
    description="Search Wikipedia for concise summaries.",
)
