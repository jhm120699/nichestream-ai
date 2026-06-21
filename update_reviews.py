import os
import re

dir_path = 'src/pages/reviews/'
if os.path.exists(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith('.md'):
            path = os.path.join(dir_path, filename)
            with open(path, 'r') as f:
                content = f.read()
            
            # Try to find product name from title
            title_match = re.search(r'title: \"(.*)\"', content)
            if title_match:
                title = title_match.group(1)
                # Heuristic: Name is after "Review of "
                if 'Review of ' in title:
                    product_name = title.split('Review of ')[-1]
                else:
                    product_name = title
                
                # Clean up product name (remove extra quotes etc)
                product_name = product_name.strip('"')
                
                if 'productName:' not in content:
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        parts[1] += f'productName: "{product_name}"\n'
                        new_content = '---' + parts[1] + '---' + parts[2]
                        with open(path, 'w') as f:
                            f.write(new_content)
                        print(f'Updated {filename} with productName: {product_name}')
else:
    print(f"Directory {dir_path} not found")
