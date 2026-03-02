from crewai import Task
from agents import job_researcher, skill_gap_analyst

# ─────────────────────────────────────────────
# TASK 1: Research live job postings
# ─────────────────────────────────────────────
job_research_task = Task(
    description=(
        "Search the internet for REAL and CURRENT job postings for the role: '{job_title}'.\n\n"
        "Search queries to use:\n"
        "- '{job_title} job requirements 2024'\n"
        "- '{job_title} skills needed LinkedIn'\n"
        "- '{job_title} job description Indeed'\n\n"
        "From the search results, extract and consolidate:\n"
        "1. Top 10 most required TECHNICAL skills\n"
        "2. Top 5 most required TOOLS / FRAMEWORKS / LIBRARIES\n"
        "3. Top 3 SOFT SKILLS mentioned\n"
        "4. Any CERTIFICATIONS or EDUCATION requirements\n"
        "5. Years of experience typically required\n\n"
        "Rank each skill by how frequently it appears across job postings.\n"
        "Label each as: 🔴 Critical | 🟡 Important | 🟢 Nice-to-have"
    ),
    expected_output=(
        "A structured list of skills required for the '{job_title}' role, "
        "categorized into Technical Skills, Tools/Frameworks, Soft Skills, "
        "and Certifications. Each skill labeled as Critical, Important, or Nice-to-have. "
        "Include frequency/demand level for each skill."
    ),
    agent=job_researcher,
)

# ─────────────────────────────────────────────
# TASK 2: Analyze skill gap and build roadmap
# ─────────────────────────────────────────────
skill_gap_task = Task(
    description=(
        "You have the job market requirements for '{job_title}' from the previous research.\n\n"
        "The user's CURRENT SKILLS are:\n"
        "{current_skills}\n\n"
        "The user's EXPERIENCE LEVEL is: {experience_level}\n\n"
        "Now perform a complete skill gap analysis:\n\n"
        "STEP 1 - SKILL MATCHING:\n"
        "  - ✅ Already Have: Skills user has that match job requirements\n"
        "  - ⚠️  Partial: Skills user has but needs to deepen\n"
        "  - ❌ Missing: Required skills user doesn't have at all\n\n"
        "STEP 2 - PRIORITY GAP LIST:\n"
        "  Rank missing skills by importance (Critical first)\n"
        "  For each missing skill provide:\n"
        "  - Why it matters for this role\n"
        "  - Estimated time to learn (weeks/months)\n"
        "  - 2-3 specific courses/resources (free + paid)\n\n"
        "STEP 3 - 90-DAY LEARNING ROADMAP:\n"
        "  - Month 1: Focus on [top priority skills]\n"
        "  - Month 2: Focus on [next priority skills]\n"
        "  - Month 3: Focus on [remaining + projects]\n\n"
        "STEP 4 - READINESS SCORE:\n"
        "  Give user a Job Readiness Score out of 100\n"
        "  Example: 'You are 62/100 ready for this role'\n\n"
        "STEP 5 - QUICK WINS:\n"
        "  List 3 things the user can do THIS WEEK to improve their profile"
    ),
    expected_output=(
        "A complete skill gap report with:\n"
        "1. Skills matching table (Have / Partial / Missing)\n"
        "2. Prioritized list of skills to learn with courses and timelines\n"
        "3. 90-day learning roadmap\n"
        "4. Job readiness score out of 100\n"
        "5. 3 quick wins for this week"
    ),
    agent=skill_gap_analyst,
    context=[job_research_task],  # Uses output from task 1
)
