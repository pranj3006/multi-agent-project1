from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re


load_dotenv(orverride=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str, max_results: int = 3) -> str:
    """Perform a web search using Tavily API and return the results."""
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")
    
    try:
        results = tavily.search(query=query, max_results=max_results)
        output=[]
        for r in results:
            output.append(
                {"url": r.get("url", "No URL provided"),
                 "title": r.get("title", "No title provided"),
                 "snippet": r.get("content", "No snippet provided")[:300]}
            )
        return "\n----\n".join(output)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@tool
def scrape_webpage(url: str) -> str:
    """Scrape the content of a webpage and return the text."""
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       " AppleWebKit/537.36 (KHTML, like Gecko)"
                       " Chrome/58.0.3029.110 Safari/537.3"),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }
    try:
        response = requests.get(url,headers=headers,timeout=15)
        
        response.raise_for_status()
        
        html_content = response.text

        # -------------------------------------------------------------
        # Strategy 1: Use trafilatura to extract text
        # -------------------------------------------------------------

        extracted_text = trafilatura.extract(
            html_content,
            include_comments=False,
            include_tables=False)

        if extracted_text and len(extracted_text.strip()) > 200:
            cleaned_text = re.sub(r'\s+', ' ', extracted_text).strip()
            return cleaned_text[:5000]

        # -------------------------------------------------------------
        # Strategy 2: Use readability-lxml to extract text
        # -------------------------------------------------------------
        doc = Document(html_content)
        cleaned_text = doc.summary()            
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(cleaned_text, 'html.parser')

        # Remove script and style elements
        for tag in soup([
            'script', 
            'style',
            'nav',
            'footer',
            'header',
            'aside',
            'form',]):
            tag.decompose()

        # Get text and clean it up
        text = soup.get_text(separator=' ',strip=True)
        
        if text and len(text.strip()) > 200:
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            return cleaned_text[:5000]

        # -------------------------------------------------------------
        # Strategy 3: Use BeautifulSoup to extract text directly from the HTML
        # -------------------------------------------------------------

        soup = BeautifulSoup( html_content  , 'html.parser')
        for tag in soup([
            'script', 
            'style',
            'nav',
            'footer',
            'header',
            'aside',
            'form',]):
            tag.decompose()

        # Get text and clean it up
        text = soup.get_text(separator=' ',strip=True)
        if text and len(text.strip()) > 200:
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            return cleaned_text[:5000]

        return "No textual content found on the page."
    except requests.exceptions.Timeout:
        return "Error: Request timed out."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}" 
    except Exception as e:
        return f"Error scraping webpage: {str(e)}"

