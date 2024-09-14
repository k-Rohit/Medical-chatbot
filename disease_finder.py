
import os
import streamlit as st
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, Process

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_MODEL_NAME"] = 'llama3-8b-8192'
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["SERPER_API_KEY"] = "bf31d18f256806e68755dbd5a79bfcf019340048"

def disease_info_page():
    st.title("Disease Information")
    
    disease = st.text_input("Enter the disease you want to know about:")
    
    if st.button("Get Information"):
        if disease:
            search_tool = SerperDevTool()
            medical_info_search_agent = Agent(
                role='Medical Information Search Specialist',
                goal=f'Find and compile the latest and most relevant information about {disease}, including symptoms, precautions, medicines, and recommended tests.',
                backstory="You excel at gathering the most current and accurate information on medical topics.",
                verbose=True,
                allow_delegation=False,
                tools=[search_tool]
            )

            reporting_analyst = Agent(
                role='Medical Reporting Analyst',
                goal='Create a detailed and well-structured report based on the findings from the Medical Information Search Specialist.',
                backstory="You are skilled in organizing complex medical information into clear, actionable reports.",
                verbose=True,
                allow_delegation=False,
            )

            medical_info_search_task = Task(
            description=f"""Perform a search to retrieve the most recent and relevant information on {disease}. 
            Gather detailed data on symptoms, precautions, medicines, and tests related to the disease.""",
            expected_output="A structured summary that includes disease name, symptoms, precautions, recommended medicines, and suggested tests.",
            agent=medical_info_search_agent
)

            reporting_task = Task(
            description="""Review and expand upon the data collected from the search. Format the information into a comprehensive markdown report with sections for symptoms, precautions, medicines, and tests. Ensure the report is clear and well-organized.""",
            expected_output="A detailed markdown report covering the disease, its symptoms, precautions, medicines, and recommended tests.",
            agent=reporting_analyst
)

            crew = Crew(
                agents=[medical_info_search_agent, reporting_analyst],
                tasks=[medical_info_search_task, reporting_task],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            report_content = result.text if hasattr(result, 'text') else str(result)
            
            st.markdown(report_content)
        else:
            st.warning("Please enter a disease name.")

if __name__ == "__main__":
    disease_info_page()
