import os

import requests

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.agents import create_agent
from src.tools.tools import web_search, scrape_webpage

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=OPENAI_API_KEY)


# Search Agent Creation
def build_search_agent():
    """Builds a search agent using the Create Agent framework."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    return create_agent(    
        model=llm,
        tools=[web_search],                
    )


# Scraper Agent Creation
def build_scraper_agent():
    """Builds a scraper agent using the Create Agent framework."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    return create_agent(
        model=llm,
        tools=[scrape_webpage],                
    )


"""Builds a writer agent using the Create Agent framework."""
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

human_message = """
Write a detailed research report on the topic below
Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all sources used in the research)

Be detailed, factual and professional.
"""
writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are an expert research writer. Write clear, structured and insightfull reports."),
    ("human",human_message)])

writer_chain = writer_prompt | llm | StrOutputParser()


"""Builds a critic agent using the Create Agent framework."""
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

human_message = """
Review the research report below and evaluated it strictly.

Report: 
{report}

Respond in this exact format:

Score: X/10

Strenghts:
- ...
- ...

Areas of Improvement:
- ...
- ...

One line verdict:
...
"""
critic_prompt = ChatPromptTemplate.from_messages([
    ("system","You are ana sharp and constructive research cirtic, be honest and specific."),
    ("human",human_message)])

critic_chain = critic_prompt | llm | StrOutputParser()

