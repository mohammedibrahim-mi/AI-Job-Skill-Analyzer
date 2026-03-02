import re
from datetime import datetime
from crewai import Crew
from agents import job_researcher, skill_gap_analyst
from tasks import job_research_task, skill_gap_task

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ============================================================
# 🎯 YOUR INPUT — SENIOR MOBILE APP DEVELOPER (5 Years)
# ============================================================

USER_NAME = "Ashok"          # ← Your name here
JOB_TITLE = "Senior Mobile App Developer"

CURRENT_SKILLS = """
MOBILE DEVELOPMENT:
- iOS Development with Swift & SwiftUI (4 years)
- Android Development with Kotlin (3 years)
- React Native (2 years — cross-platform)
- Flutter (1 year — basic)
- Xcode & Android Studio (proficient)

UI/UX IMPLEMENTATION:
- Custom UI components and animations
- Responsive layouts for multiple screen sizes
- Material Design & Apple HIG guidelines

STATE MANAGEMENT:
- Redux (React Native)
- Provider & Riverpod (Flutter)
- MVVM architecture pattern
- MVC, Clean Architecture basics

BACKEND INTEGRATION:
- REST API integration
- Firebase (Auth, Firestore, Push Notifications)
- GraphQL basics
- WebSocket for real-time features

TESTING & DEBUGGING:
- Unit testing (XCTest, JUnit)
- UI testing basics
- Crashlytics, Charles Proxy for debugging

DEVOPS & TOOLS:
- Git, GitHub, Bitbucket
- CI/CD with Fastlane & GitHub Actions
- App Store & Play Store deployment
- Agile / Scrum methodology

DATABASES:
- SQLite, Realm (local storage)
- Core Data (basic)
- Firestore (cloud)

SOFT SKILLS:
- Led a team of junior developers
- Code reviews
- Client communication
- Technical documentation
"""

EXPERIENCE_LEVEL = """
5 years of professional mobile app development experience.
Worked at 5 product companies.
Delivered 8 production apps (4 iOS, 4 cross-platform).
Currently mid-level developer targeting a Senior role at a top-tier tech company.
"""

# ============================================================
# 🚀 RUN THE CREW
# ============================================================

crew = Crew(
    agents=[job_researcher, skill_gap_analyst],
    tasks=[job_research_task, skill_gap_task],
    verbose=True,
)

print("\n" + "="*60)
print(f"🔍 Analyzing skill gap for: {JOB_TITLE}")
print(f"📅 Experience: 5 Years")
print("="*60 + "\n")

result = crew.kickoff(inputs={
    "job_title"        : JOB_TITLE,
    "current_skills"   : CURRENT_SKILLS,
    "experience_level" : EXPERIENCE_LEVEL,
})

result_text = str(result)

print("\n" + "="*60)
print("📋 SKILL GAP REPORT — SENIOR MOBILE APP DEVELOPER")
print("="*60)
print(result_text)

# ============================================================
# 📄 SAVE REPORT AS PDF
# ============================================================

def clean_text(text):
    """Remove markdown symbols for plain PDF rendering."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # italic
    text = re.sub(r'#+\s*', '', text)                 # headers
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', text)  # links
    return text.strip()

def save_report_as_pdf(report_text, job_title, user_name="", filename="skill_gap_report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    # ── Colour palette ──────────────────────────────────────
    DARK_BLUE   = colors.HexColor("#1A237E")
    MID_BLUE    = colors.HexColor("#283593")
    ACCENT      = colors.HexColor("#1565C0")
    LIGHT_BLUE  = colors.HexColor("#E3F2FD")
    GREEN       = colors.HexColor("#1B5E20")
    LIGHT_GREEN = colors.HexColor("#E8F5E9")
    ORANGE      = colors.HexColor("#E65100")
    LIGHT_ORG   = colors.HexColor("#FFF3E0")
    RED         = colors.HexColor("#B71C1C")
    LIGHT_RED   = colors.HexColor("#FFEBEE")
    GRAY_BG     = colors.HexColor("#F5F5F5")
    WHITE       = colors.white
    TEXT        = colors.HexColor("#212121")
    SUBTEXT     = colors.HexColor("#424242")

    # ── Styles ───────────────────────────────────────────────
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sTitle = S("sTitle",
        fontSize=26, leading=32, textColor=WHITE,
        alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=4)

    sSubtitle = S("sSubtitle",
        fontSize=13, leading=18, textColor=colors.HexColor("#BBDEFB"),
        alignment=TA_CENTER, fontName="Helvetica", spaceAfter=2)

    sMeta = S("sMeta",
        fontSize=10, leading=14, textColor=colors.HexColor("#90CAF9"),
        alignment=TA_CENTER, fontName="Helvetica")

    sSection = S("sSection",
        fontSize=14, leading=20, textColor=WHITE,
        fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4,
        leftIndent=6)

    sSubsection = S("sSubsection",
        fontSize=11, leading=16, textColor=ACCENT,
        fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=6)

    sBody = S("sBody",
        fontSize=10, leading=15, textColor=TEXT,
        fontName="Helvetica", spaceAfter=3, leftIndent=8)

    sBullet = S("sBullet",
        fontSize=10, leading=14, textColor=SUBTEXT,
        fontName="Helvetica", leftIndent=16, spaceAfter=2,
        bulletIndent=6)

    sLabel = S("sLabel",
        fontSize=9, leading=12, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER)

    story = []

    # ── HEADER BANNER ────────────────────────────────────────
    header_data = [[
        Paragraph("📋 Skill Gap Analysis Report", sTitle),
    ]]
    header_table = Table(header_data, colWidths=[170*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), DARK_BLUE),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING",  (0,0), (-1,-1), 18),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0), (-1,-1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4*mm))

    # sub-header row  (name | role | date)
    name_label = f"👤 {user_name}" if user_name else ""
    sub_data = [[
        Paragraph(name_label, sSubtitle),
        Paragraph(f"🎯 {job_title}", sSubtitle),
        Paragraph(f"📅 {datetime.now().strftime('%B %d, %Y')}", sMeta),
    ]]
    sub_table = Table(sub_data, colWidths=[55*mm, 75*mm, 40*mm])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), MID_BLUE),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 6*mm))

    # ── HELPER: section header bar ───────────────────────────
    def section_bar(title, bg=ACCENT):
        t = Table([[Paragraph(title, sSection)]], colWidths=[170*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), bg),
            ("TOPPADDING",   (0,0),(-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("RIGHTPADDING", (0,0),(-1,-1), 10),
            ("ROUNDEDCORNERS",[4]),
        ]))
        return t

    # ── HELPER: coloured badge pill ──────────────────────────
    def badge(text, bg, fg=WHITE):
        t = Table([[Paragraph(text, ParagraphStyle("b",
                fontSize=9, textColor=fg, fontName="Helvetica-Bold",
                alignment=TA_CENTER))]], colWidths=[30*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), bg),
            ("TOPPADDING",   (0,0),(-1,-1), 3),
            ("BOTTOMPADDING",(0,0),(-1,-1), 3),
            ("ROUNDEDCORNERS",[10]),
        ]))
        return t

    # ── PARSE RESULT INTO SECTIONS ───────────────────────────
    lines = result_text.split('\n')

    # Identify section blocks by keywords
    sections = {
        "have":    [],
        "partial": [],
        "missing": [],
        "gaps":    [],
        "roadmap": [],
        "score":   [],
        "wins":    [],
        "other":   [],
    }

    current = "other"
    for line in lines:
        ll = line.lower()
        if "already have" in ll or "✅" in ll:
            current = "have"
        elif "partial" in ll or "⚠" in ll:
            current = "partial"
        elif "missing" in ll or "❌" in ll:
            current = "missing"
        elif "priority gap" in ll or "step 2" in ll:
            current = "gaps"
        elif "90-day" in ll or "roadmap" in ll or "step 3" in ll:
            current = "roadmap"
        elif "readiness score" in ll or "step 4" in ll:
            current = "score"
        elif "quick win" in ll or "step 5" in ll:
            current = "wins"
        sections[current].append(line)

    # ── SECTION 1 : SKILL MATCHING ───────────────────────────
    story.append(section_bar("STEP 1 — Skill Matching"))
    story.append(Spacer(1, 3*mm))

    skill_cols = [
        ("✅  Already Have",  "have",    LIGHT_GREEN, GREEN),
        ("⚠️   Needs Deepening","partial", LIGHT_ORG,  ORANGE),
        ("❌  Missing",        "missing", LIGHT_RED,   RED),
    ]

    for label, key, bg, fg in skill_cols:
        items = [l for l in sections[key] if l.strip().startswith("-")]
        if not items:
            # fallback: any non-empty line
            items = [l for l in sections[key] if l.strip() and not l.lower().startswith("####")]

        header_row = [[Paragraph(label, ParagraphStyle("sh",
                fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                alignment=TA_CENTER))]]
        ht = Table(header_row, colWidths=[170*mm])
        ht.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), fg),
            ("TOPPADDING",   (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("ROUNDEDCORNERS",[3]),
        ]))
        story.append(ht)

        for item in items:
            txt = clean_text(item.strip().lstrip("-").strip())
            if txt:
                row = [[Paragraph(f"• {txt}", sBullet)]]
                rt = Table(row, colWidths=[170*mm])
                rt.setStyle(TableStyle([
                    ("BACKGROUND",   (0,0),(-1,-1), bg),
                    ("TOPPADDING",   (0,0),(-1,-1), 3),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 3),
                    ("LEFTPADDING",  (0,0),(-1,-1), 10),
                ]))
                story.append(rt)
        story.append(Spacer(1, 3*mm))

    # ── SECTION 2 : PRIORITY GAP LIST ───────────────────────
    story.append(section_bar("STEP 2 — Priority Gap List", bg=colors.HexColor("#4A148C")))
    story.append(Spacer(1, 3*mm))

    gap_lines = sections["gaps"]
    current_gap = []
    gap_blocks  = []
    for line in gap_lines:
        if re.match(r"#+\s*\d+\.", line) or re.match(r"\d+\.\s+\*\*", line):
            if current_gap:
                gap_blocks.append(current_gap)
            current_gap = [line]
        else:
            current_gap.append(line)
    if current_gap:
        gap_blocks.append(current_gap)

    priority_colors = {
        "critical":     (colors.HexColor("#D32F2F"), colors.HexColor("#FFCDD2")),
        "important":    (colors.HexColor("#F57F17"), colors.HexColor("#FFF9C4")),
        "nice-to-have": (colors.HexColor("#2E7D32"), colors.HexColor("#C8E6C9")),
    }

    for block in gap_blocks:
        if not block:
            continue
        title_line = clean_text(block[0])
        pri = "nice-to-have"
        for k in priority_colors:
            if k in title_line.lower():
                pri = k
                break
        hdr_c, bg_c = priority_colors[pri]

        # Title row
        tr = Table([[Paragraph(title_line, ParagraphStyle("gt",
                fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                leftIndent=4))]], colWidths=[170*mm])
        tr.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), hdr_c),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("ROUNDEDCORNERS",[3]),
        ]))
        story.append(tr)

        for line in block[1:]:
            txt = clean_text(line.strip().lstrip("-").strip())
            if txt:
                row = Table([[Paragraph(f"  {txt}", sBullet)]], colWidths=[170*mm])
                row.setStyle(TableStyle([
                    ("BACKGROUND",   (0,0),(-1,-1), bg_c),
                    ("TOPPADDING",   (0,0),(-1,-1), 3),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 3),
                    ("LEFTPADDING",  (0,0),(-1,-1), 12),
                ]))
                story.append(row)
        story.append(Spacer(1, 2*mm))

    # ── SECTION 3 : 90-DAY ROADMAP ──────────────────────────
    story.append(section_bar("STEP 3 — 90-Day Learning Roadmap",
                             bg=colors.HexColor("#00695C")))
    story.append(Spacer(1, 3*mm))

    month_colors = [
        colors.HexColor("#E8F5E9"),
        colors.HexColor("#E3F2FD"),
        colors.HexColor("#FFF3E0"),
    ]
    month_hdr = [
        colors.HexColor("#2E7D32"),
        colors.HexColor("#1565C0"),
        colors.HexColor("#E65100"),
    ]

    month = 0
    for line in sections["roadmap"]:
        txt = clean_text(line.strip())
        if not txt:
            continue
        if re.search(r"month\s*[123]", txt, re.I):
            idx = month % 3
            tr = Table([[Paragraph(txt, ParagraphStyle("mh",
                    fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                    leftIndent=4))]], colWidths=[170*mm])
            tr.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), month_hdr[idx]),
                ("TOPPADDING",   (0,0),(-1,-1), 6),
                ("BOTTOMPADDING",(0,0),(-1,-1), 6),
                ("LEFTPADDING",  (0,0),(-1,-1), 10),
                ("ROUNDEDCORNERS",[3]),
            ]))
            story.append(tr)
            month += 1
        elif txt.startswith("-") or txt.startswith("•"):
            idx = max(0, month-1) % 3
            row = Table([[Paragraph(f"• {txt.lstrip('-•').strip()}", sBullet)]],
                        colWidths=[170*mm])
            row.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), month_colors[idx]),
                ("TOPPADDING",   (0,0),(-1,-1), 3),
                ("BOTTOMPADDING",(0,0),(-1,-1), 3),
                ("LEFTPADDING",  (0,0),(-1,-1), 12),
            ]))
            story.append(row)
    story.append(Spacer(1, 3*mm))

    # ── SECTION 4 : READINESS SCORE ─────────────────────────
    story.append(section_bar("STEP 4 — Job Readiness Score",
                             bg=colors.HexColor("#880E4F")))
    story.append(Spacer(1, 3*mm))

    score_text = " ".join(clean_text(l) for l in sections["score"] if l.strip())
    score_match = re.search(r'(\d+)\s*/\s*100', score_text)
    score_val   = int(score_match.group(1)) if score_match else 70

    # Score bar
    bar_w    = 130*mm
    filled_w = bar_w * score_val / 100
    empty_w  = bar_w - filled_w

    score_color = (colors.HexColor("#D32F2F") if score_val < 50
                   else colors.HexColor("#F9A825") if score_val < 75
                   else colors.HexColor("#2E7D32"))

    # Numeric badge
    badge_row = Table([[
        Paragraph(f"{score_val}/100", ParagraphStyle("sc",
            fontSize=36, textColor=score_color,
            fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(
            score_text if score_text else f"You are {score_val}/100 ready for this role.",
            ParagraphStyle("sd", fontSize=11, textColor=TEXT,
                fontName="Helvetica", leading=16, leftIndent=6))
    ]], colWidths=[40*mm, 130*mm])
    badge_row.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), GRAY_BG),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("ROUNDEDCORNERS",[6]),
    ]))
    story.append(badge_row)
    story.append(Spacer(1, 3*mm))

    # ── SECTION 5 : QUICK WINS ──────────────────────────────
    story.append(section_bar("STEP 5 — Quick Wins This Week",
                             bg=colors.HexColor("#1B5E20")))
    story.append(Spacer(1, 3*mm))

    win_items = [clean_text(l.strip().lstrip("-0123456789.").strip())
                 for l in sections["wins"]
                 if l.strip() and not re.search(r"quick\s*win|step\s*5", l, re.I)]

    for i, win in enumerate(win_items[:5], 1):
        if not win:
            continue
        row = Table([[
            Paragraph(f"⚡ {i}", ParagraphStyle("wn",
                fontSize=13, textColor=WHITE, fontName="Helvetica-Bold",
                alignment=TA_CENTER)),
            Paragraph(win, sBody)
        ]], colWidths=[14*mm, 156*mm])
        row.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(0,0), colors.HexColor("#2E7D32")),
            ("BACKGROUND",   (1,0),(1,0), LIGHT_GREEN),
            ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
            ("TOPPADDING",   (0,0),(-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
            ("LEFTPADDING",  (0,0),(-1,-1), 6),
            ("RIGHTPADDING", (0,0),(-1,-1), 6),
            ("ROUNDEDCORNERS",[4]),
        ]))
        story.append(row)
        story.append(Spacer(1, 2*mm))

    # ── FOOTER ───────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=1,
                            color=colors.HexColor("#BDBDBD")))
    story.append(Spacer(1, 2*mm))
    name_str = f"Prepared for: {user_name}  •  " if user_name else ""
    story.append(Paragraph(
        f"{name_str}Generated by Skill Gap AI Agent  •  {datetime.now().strftime('%B %d, %Y at %H:%M')}  •  Role: {job_title}",
        ParagraphStyle("footer", fontSize=8, textColor=colors.HexColor("#9E9E9E"),
                       alignment=TA_CENTER, fontName="Helvetica")))

    doc.build(story)
    print(f"\n✅ PDF saved: {filename}")
    return filename


# ── Save PDF ─────────────────────────────────────────────────
pdf_path = save_report_as_pdf(result_text, JOB_TITLE,
                              user_name=USER_NAME,
                              filename="skill_gap_report.pdf")