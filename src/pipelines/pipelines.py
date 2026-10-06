from src.agents.agents import build_search_agent, build_scraper_agent, writer_chain,critic_chain

def run_research_pipeline(topic:str)->dict:
    state = {}
    
    # search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent working...")
    print("\n"+" ="*50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user",f"Find recent, reliable and detailed information about: {topic}")]})
    state["search_results"] = search_results["messages"][-1].content

    print("\n search results ",state["search_results"])


    # scrapper agent working
    print("\n"+" ="*50)
    print("step 2 - Scraper agent working...")
    print("\n"+" ="*50)

    scraper_agent = build_scraper_agent()
    scraper_results = scraper_agent.invoke({
        "messages": [("user",
        f"Based on foillowing search results about : '{topic}', "
        f"Pick the most relevant URL and scrape it for deeper content from below search results. \n\n"
        f"Search Results : \n {state['search_results'][:800]}"
        )]})
    state["scraper_results"] = scraper_results["messages"][-1].content

    print("\n scraper results ",state["scraper_results"])


    # writer chain working
    print("\n"+" ="*50)
    print("step 3 - Writer chain working...")
    print("\n"+" ="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']}\n\n"
        f"DETAILED SCRAPER RESULTS : \n {state['scraper_results']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n Final Report \n ",state["report"])


    # critic chain working
    print("\n"+" ="*50)
    print("step 4 - Critic chain working...")
    print("\n"+" ="*50)

    state["evaluation"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n Ciritic Evaluation \n ",state["evaluation"])
    return state