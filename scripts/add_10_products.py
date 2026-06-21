import subprocess
import json
import time

products = [
    {
        "name": "Notion",
        "category": "vertical-productivity",
        "description": "An all-in-one customizable workspace designed for notes, wikis, task management, and collaborative team databases.",
        "brand": "Notion Labs",
        "features": [
            ("Rich Text Editor", "Block-based editor with instant slash commands"),
            ("Collaboration", "Real-time co-editing, page sharing, and comment threads"),
            ("Wikis", "Deeply nested page hierarchies with instant cross-linking"),
            ("Databases", "Custom tables, Kanban boards, list views, and calendar integration")
        ],
        "pros": [
            "Extremely flexible, customizable, and adaptive to any workflow",
            "Thousands of pre-built community templates available",
            "Generous free tier with plenty of features for personal use"
        ],
        "cons": [
            "Learning curve can be overwhelming for new users due to high flexibility",
            "Mobile app is occasionally slower to load compared to the desktop app"
        ]
    },
    {
        "name": "Slack",
        "category": "vertical-productivity",
        "description": "A channel-based messaging platform that integrates team communication, files, and tools into one unified workspace.",
        "brand": "Salesforce",
        "features": [
            ("Channels", "Organized visual channels for projects, topics, and teams"),
            ("Huddles", "One-click audio and video screenshare calls within chats"),
            ("Integrations", "Connects out-of-the-box with Google Drive, GitHub, and Jira"),
            ("Canvas", "Collaborative documents living directly inside channel contexts")
        ],
        "pros": [
            "Real-time team messaging is blazing fast and reliable",
            "A massive app directory to automate routine workflow tasks",
            "Frictionless search engine that indexes both text and file contents"
        ],
        "cons": [
            "High message volume can lead to constant interruption and notification fatigue",
            "Free tier limits historical messages, hiding older conversations"
        ]
    },
    {
        "name": "Figma",
        "category": "vertical-productivity",
        "description": "A collaborative web-based design tool used for vector graphics, interface design, prototyping, and developer handoff.",
        "brand": "Figma Inc",
        "features": [
            ("Vector Networks", "An intuitive vector pen tool for crafting responsive shapes"),
            ("Auto Layout", "Dynamic, responsive CSS-like properties for design boxes"),
            ("Prototyping", "Create clickable micro-interactions and smart animations"),
            ("Dev Mode", "Inspect designs, export production assets, and copy styling code")
        ],
        "pros": [
            "The industry standard for real-time collaborative product design",
            "100% cloud-based, meaning zero local install friction for partners",
            "A rich community marketplace full of productivity plugins"
        ],
        "cons": [
            "Has a steep learning curve for non-designers and absolute beginners",
            "Heavy canvas files with many layers can consume high system memory"
        ]
    },
    {
        "name": "Linear",
        "category": "vertical-productivity",
        "description": "A high-performance, keyboard-first issue tracker and project management tool tailored specifically for modern software development teams.",
        "brand": "Linear App",
        "features": [
            ("Speed", "A blazing-fast SPA interface built on local cache database models"),
            ("Cycles", "Automated agile sprints, planning tools, and velocity reports"),
            ("Roadmaps", "High-level product milestone timelines and tracking boards"),
            ("Git Integration", "Automatically link, tag, and close tickets with commit branches")
        ],
        "pros": [
            "Gorgeous, clean, minimal, and entirely distraction-free UI",
            "100% keyboard shortcut coverage makes navigation incredibly fast",
            "Enforces lightweight and highly efficient sprint workflows"
        ],
        "cons": [
            "Far fewer customization features compared to platforms like Jira",
            "A very opinionated product focused strictly on software engineering teams"
        ]
    },
    {
        "name": "Zapier",
        "category": "vertical-productivity",
        "description": "An automation platform that allows non-technical users to connect and move data between thousands of different SaaS applications.",
        "brand": "Zapier",
        "features": [
            ("Multi-Step Zaps", "Chain multiple actions and triggers into automated flows"),
            ("Filters & Paths", "Create conditional logic paths and filters to refine workflows"),
            ("Webhooks", "Easily trigger workflows using standard web requests"),
            ("Formatters", "Convert dates, string patterns, or currency formats mid-flow")
        ],
        "pros": [
            "Direct out-of-the-box support for over 5,000+ popular web apps",
            "Requires absolutely zero coding or server infrastructure to operate",
            "Extremely reliable execution engine with detailed history logs"
        ],
        "cons": [
            "Can become very expensive on high-volume automated workflows",
            "Multi-step conditional paths are gated behind premium pricing tiers"
        ]
    },
    {
        "name": "Miro",
        "category": "vertical-productivity",
        "description": "An infinite collaborative online whiteboard that helps teams brainstorm, map out workflows, and visually plan projects.",
        "brand": "RealtimeBoard Inc",
        "features": [
            ("Infinite Canvas", "An endless digital canvas with freeform drawing and stickies"),
            ("Template Library", "Pre-built templates for mind maps, user flows, and mockups"),
            ("Workshop Tools", "In-app voting, session timers, and cursor tracking options"),
            ("Smart Drawing", "Automatically refine freehand lines into crisp vector shapes")
        ],
        "pros": [
            "Outstanding experience for visual remote collaboration and workshops",
            "Highly responsive and intuitive real-time cursor tracking system",
            "Integrates seamlessly with agile tools like Jira, Confluence, and Slack"
        ],
        "cons": [
            "Navigating huge boards with hundreds of media objects can lag slightly",
            "Does not support full offline viewing or creation modes"
        ]
    },
    {
        "name": "Loom",
        "category": "vertical-productivity",
        "description": "An async video messaging platform designed to let you record your screen, camera, and voice with instant shareable link creation.",
        "brand": "Loom",
        "features": [
            ("Screen Recording", "Capture your desktop browser, specific windows, and camera"),
            ("Instant Link", "Share link is automatically copied to your clipboard on stop"),
            ("Video Editing", "Directly trim video frames and remove filler words in-app"),
            ("AI Transcripts", "Automated text transcripts, summaries, and title generation")
        ],
        "pros": [
            "Significantly reduces real-time calendar fatigue and meetings",
            "Allows for extremely quick visual explanations and walk-throughs",
            "Polished web and browser extension integrations with fast upload speeds"
        ],
        "cons": [
            "Free tiers limit video recordings to exactly 5 minutes each",
            "Audio processing can sound compressed without dedicated microphones"
        ]
    },
    {
        "name": "ClickUp",
        "category": "vertical-productivity",
        "description": "An all-in-one project management hub designed to centralize tasks, docs, goals, chat, and wikis into a single workspace.",
        "brand": "Mango Technologies",
        "features": [
            ("Hierarchical Lists", "Organize elements using lists, folders, and dedicated spaces"),
            ("Custom Views", "Instantly toggle between list, Kanban board, Gantt, and mindmaps"),
            ("Integrated Docs", "Draft wiki pages, knowledge bases, and connect tasks internally"),
            ("Goals & OKRs", "Establish targets and automatically aggregate nested task metrics")
        ],
        "pros": [
            "Replaces multiple standalone SaaS products in one single bill",
            "Incredibly robust feature set and template engine",
            "Clean dashboard reporting widgets for executive-level oversight"
        ],
        "cons": [
            "Sheer volume of features can create a cluttered and complex UI",
            "Requires substantial upfront investment to configure templates properly"
        ]
    },
    {
        "name": "Trello",
        "category": "vertical-productivity",
        "description": "A visual, drag-and-drop Kanban board tool that lets you manage projects and organize everyday tasks dynamically.",
        "brand": "Atlassian",
        "features": [
            ("Kanban Boards", "Organize cards across columns like Todo, In Progress, and Done"),
            ("Power-Ups", "Enhance boards with calendars, custom fields, and Slack links"),
            ("Butler Automation", "No-code workflow bot for recurring tasks and reminders"),
            ("Card Templates", "Pre-set descriptions, checklists, and labels for standard tasks")
        ],
        "pros": [
            "Extremely low barrier to entry; team onboarding is nearly instant",
            "Highly visual card-based interface with satisfying drag animations",
            "Lightweight, snappy, and works beautifully across devices"
        ],
        "cons": [
            "Lacks the complex scheduling, dependency paths, and budgets of Gantt charts",
            "Boards with massive card volumes can become challenging to scan"
        ]
    },
    {
        "name": "Airtable",
        "category": "vertical-productivity",
        "description": "A cloud platform that marries the simplicity of an online spreadsheet with the robust relational capabilities of a database.",
        "brand": "Airtable",
        "features": [
            ("Relational Tables", "Link records between sheets to maintain database integrity"),
            ("Interface Designer", "Build custom drag-and-drop mini apps for other team members"),
            ("Form Views", "Collect customer inputs directly into rows with custom forms"),
            ("Automations", "Trigger actions in external tools when row status changes")
        ],
        "pros": [
            "Provides spreadsheet users with the capabilities of a robust database",
            "Ideal for creating internal asset trackers, CRM platforms, and content hubs",
            "Excellent native developer API for custom integrations and scripting"
        ],
        "cons": [
            "Pricing per collaborator is expensive compared to generic spreadsheet apps",
            "Strict row limits on basic workspaces require planning for long-term data"
        ]
    }
]

def run_sql(sql):
    cmd = ["team-db", sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SQL Error: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout

print("Starting import of 10 modern SaaS tools...")

for p in products:
    name_esc = p["name"].replace("'", "''")
    cat_esc = p["category"].replace("'", "''")
    brand_esc = p["brand"].replace("'", "''")
    desc_esc = p["description"].replace("'", "''")
    
    # Insert Product
    sql_prod = f"""
    INSERT INTO products (name, category, brand, description)
    VALUES ('{name_esc}', '{cat_esc}', '{brand_esc}', '{desc_esc}')
    """
    print(f"Inserting product: {p['name']}...")
    run_sql(sql_prod)
    
    # Fetch inserted product id
    sql_get_id = f"SELECT id FROM products WHERE name='{name_esc}' ORDER BY id DESC LIMIT 1"
    res_id = run_sql(sql_get_id)
    if not res_id or not isinstance(res_id, list):
        print(f"Error fetching id for {p['name']}. Skipping child tables.")
        continue
    p_id = res_id[0]["id"]
    print(f"Product {p['name']} inserted with ID: {p_id}")
    
    # Insert Features
    for feat_name, feat_val in p["features"]:
        feat_name_esc = feat_name.replace("'", "''")
        feat_val_esc = feat_val.replace("'", "''")
        sql_feat = f"""
        INSERT INTO product_features (product_id, feature_name, feature_value)
        VALUES ({p_id}, '{feat_name_esc}', '{feat_val_esc}')
        """
        run_sql(sql_feat)
        
    # Insert Pros
    for pro in p["pros"]:
        pro_esc = pro.replace("'", "''")
        sql_pro = f"""
        INSERT INTO product_pros (product_id, pro_text)
        VALUES ({p_id}, '{pro_esc}')
        """
        run_sql(sql_pro)
        
    # Insert Cons
    for con in p["cons"]:
        con_esc = con.replace("'", "''")
        sql_con = f"""
        INSERT INTO product_cons (product_id, con_text)
        VALUES ({p_id}, '{con_esc}')
        """
        run_sql(sql_con)

print("Successfully imported all 10 products into Turso database!")
