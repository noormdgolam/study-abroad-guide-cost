import os
import json
import random
from datetime import datetime, timedelta

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

articles_dir = os.path.join('_src', 'content', 'articles')
pages_dir = os.path.join('_src', 'content', 'pages')

os.makedirs(articles_dir, exist_ok=True)
os.makedirs(pages_dir, exist_ok=True)

categories = ['tuition', 'living-costs', 'scholarships', 'visas']
destinations = ['US', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Japan', 'South Korea']
majors = ['Engineering', 'Business', 'Computer Science', 'Medicine', 'Arts', 'Law']

# Generate pillar articles
pillars = [
    {
        "title": "The Ultimate Guide to US vs UK Study Abroad Costs (2026)",
        "slug": "us-vs-uk-study-abroad-costs",
        "category": "tuition",
        "is_pillar": "true",
        "content": "A detailed breakdown of tuition fees, living expenses, and hidden costs when choosing between the US and UK for your studies. \n\n## Tuition Fees Comparison\nIn the US, tuition can range from $20,000 to $60,000 per year. The UK typically ranges from £10,000 to £38,000. \n\n## Living Costs\nLiving in London vs New York City."
    },
    {
        "title": "Complete Breakdown of Living Costs for International Students",
        "slug": "international-student-living-costs-breakdown",
        "category": "living-costs",
        "is_pillar": "true",
        "content": "An exhaustive look into rent, food, transport, and entertainment across top destinations. \n\n## Housing\nOn-campus vs Off-campus. \n\n## Food\nGroceries vs Eating Out."
    },
    {
        "title": "How to Find and Apply for Full-Ride Scholarships Abroad",
        "slug": "full-ride-scholarships-abroad-guide",
        "category": "scholarships",
        "is_pillar": "true",
        "content": "A step-by-step guide to securing merit-based and need-based financial aid. \n\n## Government Scholarships\nFulbright, Chevening, etc. \n\n## University Grants\nHow to negotiate."
    },
    {
        "title": "Student Visa Costs and Financial Proof Requirements by Country",
        "slug": "student-visa-costs-financial-proof",
        "category": "visas",
        "is_pillar": "true",
        "content": "What you need to pay upfront and how much you need in your bank account to get approved. \n\n## US F-1 Visa\nSEVIS fee and application fee. \n\n## UK Tier 4 Visa\nHealthcare surcharge."
    }
]

for p in pillars:
    frontmatter = f"""---
title: "{p['title']}"
slug: "{p['slug']}"
category: "{p['category']}"
author: "Editorial Team"
date: "2026-07-10"
is_pillar: {p['is_pillar']}
key_takeaways:
  - "Understand the major differences between destinations."
  - "Plan your budget early to avoid surprises."
  - "Always check for updated fees on official university websites."
---
{p['content']}
"""
    create_file(os.path.join(articles_dir, f"{p['slug']}.md"), frontmatter)

# Generate 96 long-tail dummy articles
for i in range(1, 97):
    dest = random.choice(destinations)
    cat = random.choice(categories)
    major = random.choice(majors)
    
    title = f"Cost of Studying {major} in {dest}: {2026 if i%2==0 else 2025} Guide"
    slug = f"cost-of-studying-{major.lower().replace(' ', '-')}-in-{dest.lower().replace(' ', '-')}-{i}"
    
    date = (datetime.now() - timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
    
    frontmatter = f"""---
title: "{title}"
slug: "{slug}"
category: "{cat}"
author: "Jane Doe"
date: "{date}"
is_pillar: false
key_takeaways:
  - "Tuition for {major} in {dest} varies by university rank."
  - "Cost of living heavily depends on the city."
  - "Look out for specific departmental scholarships."
---
Studying {major} in {dest} is a dream for many. But how much does it actually cost? In this guide, we break down the {cat} associated with this path.

## Understanding the Fees
The costs can be divided into several components.

## Hidden Costs
Don't forget about insurance, books, and travel.

## Conclusion
Plan ahead to make your study abroad journey smooth.
"""
    create_file(os.path.join(articles_dir, f"{slug}.md"), frontmatter)

# Generate basic pages
pages = [
    {"title": "About Us", "slug": "about", "content": "Welcome to Study Abroad Guide Guide. We are dedicated to providing transparent cost comparisons."},
    {"title": "Contact", "slug": "contact", "content": "Reach us at contact@bongshai.com."},
    {"title": "Privacy Policy", "slug": "privacy", "content": "We use Google AdSense and cookies to personalize content and ads."},
    {"title": "Terms of Service", "slug": "terms", "content": "By using our site, you agree to our terms."},
    {"title": "Disclaimer", "slug": "disclaimer", "content": "The content provided is for informational purposes only. We are not financial or immigration advisors."}
]

for p in pages:
    frontmatter = f"""---
title: "{p['title']}"
slug: "{p['slug']}"
---
{p['content']}
"""
    create_file(os.path.join(pages_dir, f"{p['slug']}.md"), frontmatter)

print("Dummy content generated successfully. Total articles:", 4 + 96)
