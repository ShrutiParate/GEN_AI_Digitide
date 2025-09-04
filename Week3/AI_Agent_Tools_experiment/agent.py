import os
from dotenv import load_dotenv

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor


# 1. Load API Keys
load_dotenv()  # Reads from .env file


# 2. Setup Google Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Gemini LLM
    temperature=0.7
)


# 3. Define Tools

# Calculator Tool
@tool
def calculator(query: str) -> str:
    """Useful for solving math problems. Input should be a mathematical expression."""
    try:
        result = eval(query, {"__builtins__": {}}, {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "len": len,
            "int": int, "float": float, "str": str
        })
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Web Search Tool using SerpAPI
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

@tool
def search_tool(query: str) -> str:
    """Useful for searching the web for current information, news, facts, and general queries."""
    try:
        result = search.run(query)
        return result
    except Exception as e:
        return f"Search error: {e}"

# Register tools
tools = [calculator, search_tool]


# 4. Create ReAct Agent
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

# Executor (runs the agent loop)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,              # shows reasoning steps
    handle_parsing_errors=True,
    max_iterations=5           # safety: don’t loop forever
)


# 5. Run in Terminal
if __name__ == "__main__":
    print("=== AI Agent with Google Gemini + SerpAPI ===")
    print("Available tools: Calculator, Web Search")
    print("Examples:")
    print("- 'What is 25 * 47 + 123?'")
    print("- 'Search for latest news about AI'")
    print("- 'What is the weather like in Nagpur today?'")

    while True:
        try:
            query = input("\nEnter your query (or 'exit'): ")
            if query.lower() == "exit":
                print("Goodbye!")
                break

            # Run agent
            response = agent_executor.invoke({"input": query})
            print("\n🤖 Agent Response:", response["output"])

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or type 'exit' to quit.")
