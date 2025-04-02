from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# TAVILY_API_KEY = "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"


# tavily_api_wrapper = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)
# tools = [TavilySearchResults(api_wrapper=tavily_api_wrapper, max_results=3)]
# # Choose the LLM that will drive the agent
# llm = ChatOpenAI(model="gpt-4-turbo-preview")
# prompt = "You are a helpful assistant."
# agent_executor = create_react_agent(llm, tools, prompt=prompt)

