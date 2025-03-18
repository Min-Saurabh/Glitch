def detect_language(query: str) -> str:
    # Define keywords for the specified programming languages
    language_keywords = {
        "python": ["def ", "import ", "print(", "lambda"],
        "java": ["public static void main", "class ", "import "],
        "c": ["int main", "#include", "printf("],
        "cpp": ["#include", "using namespace std;", "int main"],
    }

    # Check the query for keywords to determine the language
    for language, keywords in language_keywords.items():
        if any(keyword in query for keyword in keywords):
            return language

    return "txt"  # Default to 'txt' if no keywords match