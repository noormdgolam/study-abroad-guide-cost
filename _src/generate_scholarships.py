import os
import re
from datetime import datetime

articles_dir = os.path.join('_src', 'content', 'articles')
os.makedirs(articles_dir, exist_ok=True)

scholarships = [
    # UK
    ("Chevening Scholarships", "UK", "UK Government", "Fully Funded", "Master's"),
    ("Rhodes Scholarships", "UK", "Oxford University", "Fully Funded", "Postgraduate"),
    ("Gates Cambridge Scholarships", "UK", "Cambridge University", "Fully Funded", "Postgraduate"),
    ("Clarendon Fund Scholarships", "UK", "Oxford University", "Fully Funded", "Postgraduate"),
    ("Reach Oxford Scholarships", "UK", "Oxford University", "Tuition & Living", "Undergraduate"),
    ("Edinburgh Global Research Scholarships", "UK", "University of Edinburgh", "Tuition difference", "PhD"),
    ("Bristol Think Big Scholarships", "UK", "Bristol University", "Partial Tuition", "Undergrad/Postgrad"),
    ("Sheffield International Merit Scholarships", "UK", "University of Sheffield", "Partial Tuition", "Undergrad/Postgrad"),
    ("Nottingham Developing Solutions Scholarships", "UK", "University of Nottingham", "Partial/Full Tuition", "Master's"),
    ("Warwick Chancellor's International Scholarships", "UK", "University of Warwick", "Full Tuition & Stipend", "PhD"),
    ("UCL Global Masters Scholarships", "UK", "University College London", "Partial Tuition", "Master's"),
    ("Westminster International Scholarships", "UK", "University of Westminster", "Full Tuition, Living, Flights", "Master's"),
    ("Cardiff University Vice-Chancellor's International Scholarships", "UK", "Cardiff University", "Partial Tuition", "Undergrad/Postgrad"),
    ("Swansea University Excellence Scholarships", "UK", "Swansea University", "Partial Tuition", "Undergrad/Postgrad"),
    
    # US
    ("Fulbright Foreign Student Program", "US", "US Government", "Fully Funded", "Master's/PhD"),
    ("Knight-Hennessy Scholars", "US", "Stanford University", "Fully Funded", "Postgraduate"),
    ("Yale University Scholarships", "US", "Yale University", "Need-Based Fully Funded", "Undergraduate"),
    ("Harvard University Financial Aid", "US", "Harvard University", "Need-Based Fully Funded", "Undergraduate"),
    ("MIT Financial Aid", "US", "MIT", "Need-Based Fully Funded", "Undergraduate"),
    ("Amherst College International Scholarships", "US", "Amherst College", "Need-Based Fully Funded", "Undergraduate"),
    ("Clark Global Scholars Program", "US", "Clark University", "Partial Tuition", "Undergraduate"),
    ("AU Emerging Global Leader Scholarship", "US", "American University", "Full Tuition, Room & Board", "Undergraduate"),
    ("Columbia University Scholarships", "US", "Columbia University", "Need-Based Fully Funded", "Undergraduate"),
    ("Cornell University Financial Aid", "US", "Cornell University", "Need-Based Fully Funded", "Undergraduate"),
    ("Dartmouth College Scholarships", "US", "Dartmouth College", "Need-Based Fully Funded", "Undergraduate"),
    ("NYU Wagner Scholarships", "US", "New York University", "Partial/Full Tuition", "Master's"),
    ("Illinois Wesleyan University Scholarships", "US", "Illinois Wesleyan University", "Partial/Full Tuition", "Undergraduate"),
    ("Berea College Scholarships", "US", "Berea College", "100% Fully Funded First Year", "Undergraduate"),
    
    # Canada
    ("Banting Postdoctoral Fellowships", "Canada", "Canadian Government", "$70,000/year", "Postdoctoral"),
    ("Vanier Canada Graduate Scholarships", "Canada", "Canadian Government", "$50,000/year", "PhD"),
    ("Lester B. Pearson International Scholarships", "Canada", "University of Toronto", "Fully Funded", "Undergraduate"),
    ("UBC Karen McKellin International Leader of Tomorrow", "Canada", "University of British Columbia", "Need/Merit Based", "Undergraduate"),
    ("Calgary International Entrance Scholarships", "Canada", "University of Calgary", "$15,000/year", "Undergraduate"),
    ("Waterloo International Master's Award", "Canada", "University of Waterloo", "$2,500/term", "Master's"),
    ("McGill University Entrance Scholarships", "Canada", "McGill University", "$3,000 to $12,000", "Undergraduate"),
    ("Dalhousie University Scholarships", "Canada", "Dalhousie University", "Varies", "Undergrad/Postgrad"),
    ("Manitoba Graduate Fellowships", "Canada", "University of Manitoba", "$14,000 to $18,000", "Master's/PhD"),
    ("Pierre Elliott Trudeau Foundation Scholarships", "Canada", "Trudeau Foundation", "$40,000/year + travel", "PhD"),
    ("York University International Student Scholarships", "Canada", "York University", "Up to $140,000", "Undergraduate"),
    ("Carleton University Entrance Scholarships", "Canada", "Carleton University", "Up to $16,000", "Undergraduate"),

    # Australia & New Zealand
    ("Australia Awards Scholarships", "Australia", "Australian Government", "Fully Funded", "Undergrad/Postgrad"),
    ("Destination Australia", "Australia", "Australian Government", "$15,000/year", "Undergrad/Postgrad"),
    ("Research Training Program (RTP)", "Australia", "Australian Government", "Full Tuition & Stipend", "Postgraduate"),
    ("Sydney Scholars India Scholarship", "Australia", "University of Sydney", "Up to $500,000 total", "Undergrad/Postgrad"),
    ("Melbourne Research Scholarships", "Australia", "University of Melbourne", "Full Tuition & Stipend", "Master's/PhD"),
    ("Monash International Merit Scholarships", "Australia", "Monash University", "$10,000/year", "Undergrad/Postgrad"),
    ("Adelaide Global Academic Excellence Scholarships", "Australia", "University of Adelaide", "50% Tuition", "Undergrad/Postgrad"),
    ("UWA Global Excellence Scholarship", "Australia", "UWA", "Up to $48,000", "Undergrad/Postgrad"),
    ("Griffith Remarkable Scholarship", "Australia", "Griffith University", "50% Tuition", "Undergrad/Postgrad"),
    ("Macquarie Vice-Chancellor's International Scholarship", "Australia", "Macquarie University", "Up to $10,000", "Undergrad/Postgrad"),
    ("New Zealand Scholarships", "New Zealand", "NZ Government", "Fully Funded", "Undergrad/Postgrad"),
    ("University of Auckland International Excellence", "New Zealand", "University of Auckland", "Up to $10,000", "Undergrad/Postgrad"),

    # Europe & Asia
    ("Erasmus Mundus Joint Master Degrees", "Europe", "EU Commission", "Fully Funded", "Master's"),
    ("Eiffel Excellence Scholarship Programme", "France", "French Ministry for Europe", "Monthly Allowance", "Master's/PhD"),
    ("DAAD Scholarships", "Germany", "DAAD", "Monthly Allowance", "Master's/PhD"),
    ("ETH Zurich Excellence Scholarship", "Switzerland", "ETH Zurich", "Partial Tuition & Stipend", "Master's"),
    ("Amsterdam Excellence Scholarships", "Netherlands", "University of Amsterdam", "€25,000", "Master's"),
    ("Swedish Institute Scholarships for Global Professionals", "Sweden", "Swedish Institute", "Fully Funded", "Master's"),
    ("MEXT Scholarships", "Japan", "Japanese Government", "Fully Funded", "Undergrad/Postgrad"),
    ("Global Korea Scholarship (GKS)", "South Korea", "Korean Government", "Fully Funded", "Undergrad/Postgrad"),
    ("Chinese Government Scholarships (CSC)", "China", "Chinese Government", "Fully Funded", "Undergrad/Postgrad"),
    ("Swiss Government Excellence Scholarships", "Switzerland", "Swiss Government", "Monthly Allowance", "Postgrad/Postdoctoral"),
    ("Orange Knowledge Programme", "Netherlands", "Nuffic", "Fully Funded", "Short Courses/Master's"),
    ("Emile Boutmy Scholarships", "France", "Sciences Po", "Up to €14,210", "Undergrad/Master's"),
    ("Radboud Scholarship Programme", "Netherlands", "Radboud University", "Partial Tuition", "Master's"),
    ("Utrecht Excellence Scholarships", "Netherlands", "Utrecht University", "Tuition & Living", "Master's"),
    ("Leiden University Excellence Scholarship (LExS)", "Netherlands", "Leiden University", "Tuition fee reduction", "Master's"),
    ("VLIR-UOS Training and Masters Scholarships", "Belgium", "VLIR-UOS", "Fully Funded", "Master's"),
    ("KU Leuven Science Scholarships", "Belgium", "KU Leuven", "Up to €10,000", "Master's"),
    ("Chalmers IPOET Scholarships", "Sweden", "Chalmers University", "75% Tuition", "Master's"),
    ("KTH Royal Institute of Technology Scholarships", "Sweden", "KTH", "Partial/Full Tuition", "Master's"),
    ("Lund University Global Scholarship", "Sweden", "Lund University", "Partial/Full Tuition", "Undergrad/Master's"),
    ("Danish Government Scholarships", "Denmark", "Danish Ministry", "Tuition & Grant", "Master's"),
    ("A*STAR SINGA", "Singapore", "A*STAR", "Fully Funded", "PhD"),
    ("NTU Nanyang President's Graduate Scholarship", "Singapore", "NTU", "Fully Funded", "PhD"),
    
    # Global / Organization-based
    ("Joint Japan World Bank Graduate Scholarship", "Global", "World Bank", "Fully Funded", "Master's"),
    ("Aga Khan Foundation International Scholarship", "Global", "Aga Khan Foundation", "50% Grant / 50% Loan", "Master's/PhD"),
    ("Rotary Foundation Global Grant Scholarships", "Global", "Rotary Foundation", "Up to $30,000", "Master's/PhD"),
    ("OPEC Fund for International Development (OFID)", "Global", "OFID", "Fully Funded", "Master's")
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

date_str = datetime.now().strftime('%Y-%m-%d')

for idx, sch in enumerate(scholarships):
    name, country, org, coverage, level = sch
    slug = slugify(f"{name}-{country}")
    
    # Generic realistic content
    content = f"""---
title: "How to Apply for the {name} ({country})"
slug: "{slug}"
category: "scholarships"
author: "Editorial Team"
date: "{date_str}"
is_pillar: false
key_takeaways:
  - "Offered by: {org}"
  - "Study Level: {level}"
  - "Coverage: {coverage}"
---
The **{name}** is one of the most prestigious opportunities for international students looking to study in {country}. If you are planning your study abroad journey and need financial support, this scholarship should be at the top of your list.

## Overview of the {name}
Provided by {org}, this scholarship program aims to attract the brightest minds from around the world. Securing this funding can significantly reduce the financial burden of international education. 

### What Does it Cover?
The scholarship provides **{coverage}** for eligible students pursuing a {level} degree. Depending on the exact terms for the current academic year, this may include:
- Tuition fee waivers (partial or full)
- A monthly living stipend
- Health insurance coverage
- Airfare allowances (if applicable)

## Eligibility Requirements
While specific requirements change slightly every application cycle, successful candidates typically demonstrate:
1. **Academic Excellence:** High GPA or equivalent in your previous studies.
2. **Leadership Potential:** A track record of extracurricular leadership or community impact.
3. **Language Proficiency:** Depending on the program, you may need IELTS, TOEFL, or local language certifications.
4. **Residency:** You must be an international student meeting the specific citizenship criteria outlined by {org}.

## How to Apply: Step-by-Step

### Step 1: Research Deadlines
Deadlines for the {name} vary depending on your home country and the specific university you are applying to. **Always check the official website** months in advance.

### Step 2: Prepare Documentation
You will likely need:
- Certified academic transcripts
- A compelling Statement of Purpose (SOP) or Personal Statement
- 2-3 Letters of Recommendation (Academic or Professional)
- Proof of English/local language proficiency

### Step 3: Secure Admission (If Required)
For many university-specific scholarships, you must first apply and secure an unconditional offer of admission for your {level} program before you can apply for the scholarship.

### Step 4: Submit the Application
Follow the instructions on the official {org} portal. Ensure all documents are uploaded in the correct format before the cutoff time.

## Conclusion
The {name} in {country} is highly competitive, but the reward is life-changing. Start your preparation early, tailor your personal statement to the values of {org}, and don't hesitate to reach out to alumni for advice.
"""
    
    file_path = os.path.join(articles_dir, f"{slug}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Generated {len(scholarships)} real scholarship pages successfully.")
