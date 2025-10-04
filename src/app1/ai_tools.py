from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_tavily import TavilySearch
import requests
from bs4 import BeautifulSoup

# -------------------------------
# Tool 1: TavilySearchTool
# -------------------------------
class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Search query for TavilySearch")
    max_results: int = Field(1, description="Maximum number of search results")

class TavilySearchTool(BaseTool):
    name: str = "TavilySearchTool"
    description: str = "Search the web using TavilySearch and return textual results"
    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str, max_results: int = 1) -> str:
        searcher = TavilySearch(max_results=max_results)
        return searcher.run(query)


# -------------------------------
# Tool 2: ProcessSearchTool
# -------------------------------
class ProcessSearchInput(BaseModel):
    url: str = Field(..., description="URL of the webpage to process")

class ProcessSearchTool(BaseTool):
    name: str = "ProcessSearchTool"
    description: str = "Fetch and process HTML content from a URL, returning plain text"
    args_schema: Type[BaseModel] = ProcessSearchInput

    def _run(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()