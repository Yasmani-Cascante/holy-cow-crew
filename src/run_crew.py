from crewai import Agent, Task, Crew, Process
from agents.performance_analysis_agent import PerformanceAnalysisAgent
from agents.marketing_agent import MarketingAgent
from textwrap import dedent

def create_crew():
    # Initialize agents
    performance_agent = PerformanceAnalysisAgent().get_agent()
    marketing_agent = MarketingAgent().get_agent()
    
    # Create tasks
    performance_task = Task(
        description=dedent("""Analyze sales performance and provide insights:
        1. Review prediction accuracy
        2. Analyze performance patterns
        3. Provide optimization recommendations"""),
        agent=performance_agent,
        expected_output=dedent("""A detailed performance analysis including:
        - Prediction accuracy metrics
        - Performance patterns identified
        - Specific recommendations for improvement""")
    )

    marketing_task = Task(
        description=dedent("""Develop marketing strategy for Zurich:
        1. Analyze local demographics
        2. Identify key target segments
        3. Recommend marketing channels and tactics"""),
        agent=marketing_agent,
        expected_output=dedent("""A comprehensive marketing strategy including:
        - Demographic analysis
        - Target segment identification
        - Marketing channels and tactics
        - Implementation recommendations""")
    )

    # Create and return crew
    crew = Crew(
        agents=[performance_agent, marketing_agent],
        tasks=[performance_task, marketing_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

if __name__ == "__main__":
    crew = create_crew()
    result = crew.kickoff()
    print("\nFinal Results:")
    print(result)