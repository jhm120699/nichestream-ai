import os
import json

base_dir = "/home/team/shared/nichestream-ai/src/pages/reviews"
files_to_fix = [
    "airtable.md", "clickup.md", "figma.md", "linear.md", "loom.md",
    "miro.md", "notion.md", "slack.md", "trello.md", "zapier.md"
]

for filename in files_to_fix:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    print(f"Re-processing {filename}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split('---', 2)
    if len(parts) < 3:
        if content.startswith('---'):
            parts = content[3:].split('---', 1)
            if len(parts) == 2:
                parts = ['', parts[0], parts[1]]
            else:
                print(f"Could not split frontmatter for {filename}")
                continue
        else:
            print(f"Could not split frontmatter for {filename}")
            continue
            
    frontmatter_raw = parts[1]
    markdown_content = parts[2]
    
    # Parse line by line
    lines = frontmatter_raw.split('\n')
    cleaned_lines = []
    
    in_json_ld = False
    json_ld_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.startswith('json_ld:'):
            in_json_ld = True
            cleaned_lines.append("json_ld: |")
            continue
            
        if in_json_ld:
            json_ld_lines.append(stripped)
        else:
            if 'json_ld:' in stripped:
                key_part, json_part = stripped.split('json_ld:', 1)
                if key_part.strip():
                    cleaned_lines.append(key_part.strip())
                cleaned_lines.append("json_ld: |")
                in_json_ld = True
            else:
                cleaned_lines.append(stripped)
                
    # Parse and format the json_ld content
    if json_ld_lines:
        json_str = '\n'.join(json_ld_lines)
        try:
            start_idx = json_str.find('{')
            end_idx = json_str.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = json_str[start_idx:end_idx+1]
            json_obj = json.loads(json_str)
            formatted_json = json.dumps(json_obj, indent=2)
            indented_json = '\n'.join('  ' + line for line in formatted_json.split('\n'))
            cleaned_lines.append(indented_json)
        except Exception as e:
            print(f"Error parsing JSON for {filename}: {e}. Fallback to lines.")
            indented_json = '\n'.join('  ' + line for line in json_ld_lines)
            cleaned_lines.append(indented_json)
            
    new_frontmatter = '\n'.join(cleaned_lines)
    new_content = f"---\n{new_frontmatter}\n---\n{markdown_content}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully re-fixed {filename}")
