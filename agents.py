import os
from crewai import Agent
from crewai.llm import LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
    max_tokens=500,
    timeout=120
)

# Web search tool (requires SERPER_API_KEY in .env)
search_tool = SerperDevTool()

# ─────────────────────────────────────────────
# AGENT 1: Job Researcher
# Searches live job postings and extracts required skills
# ─────────────────────────────────────────────
job_researcher = Agent(
    role="Job Market Researcher",
    goal=(
        "Search the internet for real, current job postings for the given job title. "
        "Extract the top required skills, qualifications, tools, and technologies "
        "that appear most frequently across multiple job listings."
    ),
    llm=llm,
    tools=[search_tool],
    backstory=(
        "You are an expert job market researcher with years of experience analyzing "
        "job descriptions across LinkedIn, Indeed, Glassdoor, and company career pages. "
        "You know how to identify the most in-demand skills for any role by scanning "
        "multiple real job postings. You always search for at least 5 different postings "
        "and consolidate the most common requirements into a clean, ranked skill list. "
        "You separate skills into: Technical Skills, Tools/Frameworks, Soft Skills, "
        "and Certifications/Education."
    ),
    verbose=True,
)

# ─────────────────────────────────────────────
# AGENT 2: Skill Gap Analyst
# Compares job requirements vs user's current skills
# ─────────────────────────────────────────────
skill_gap_analyst = Agent(
    role="Career Skill Gap Analyst",
    goal=(
        "Compare the job market requirements against the user's current skills. "
        "Identify exactly what skills are missing, partially known, or already strong. "
        "Provide a prioritized learning roadmap with specific courses and resources."
    ),
    llm=llm,
    backstory=(
        "You are a senior career coach and technical skills assessor who has helped "
        "thousands of professionals land their dream jobs. You are brilliant at: \n"
        "1. Mapping user skills against job requirements\n"
        "2. Identifying critical gaps vs nice-to-have gaps\n"
        "3. Prioritizing what to learn first for maximum job impact\n"
        "4. Recommending specific, free and paid courses (Coursera, Udemy, YouTube, "
        "official docs, etc.)\n"
        "5. Giving realistic timelines to bridge each skill gap\n"
        "You always output a clear, structured report the user can act on immediately."
    ),
    verbose=True,
)
