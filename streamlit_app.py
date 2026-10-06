import streamlit as st

from src.pipelines.pipelines import run_research_pipeline


st.set_page_config(page_title="Research Agent", page_icon=":material/search:", layout="wide")
st.title("Multi-Agent Research")
st.caption("Run a topic through search, scraping, report writing, and review.")

with st.form("research_form"):
    topic = st.text_input("Research topic", placeholder="e.g. Recent advances in battery recycling")
    submitted = st.form_submit_button("Run research", type="primary")

if submitted:
    if not topic.strip():
        st.warning("Enter a topic to start the research pipeline.")
    else:
        st.session_state.pop("research_results", None)
        with st.spinner("Running the research pipeline..."):
            try:
                st.session_state.research_results = run_research_pipeline(topic.strip())
                st.session_state.research_topic = topic.strip()
                st.session_state.research_error = None
            except Exception as error:
                st.session_state.research_error = str(error)

if st.session_state.get("research_error"):
    st.error(f"Research pipeline failed: {st.session_state.research_error}")

results = st.session_state.get("research_results")
if results:
    st.subheader(f"Results: {st.session_state.get('research_topic', 'latest run')}")
    search_tab, scrape_tab, report_tab, critique_tab = st.tabs(
        ["Search results", "Scraped details", "Research report", "Critic evaluation"]
    )

    with search_tab:
        st.markdown(results.get("search_results", "No search results were returned."))
    with scrape_tab:
        st.markdown(results.get("scraper_results", "No scraped details were returned."))
    with report_tab:
        st.markdown(results.get("report", "No report was returned."))
    with critique_tab:
        st.markdown(results.get("evaluation", "No evaluation was returned."))