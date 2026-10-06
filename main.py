from src.pipelines.pipelines import run_research_pipeline

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    results = run_research_pipeline(topic)
    print("\nFinal Results:")
    print(results)