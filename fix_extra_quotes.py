import os
import re

TEMPLATE_DIR = 'questionarios/templates'
# Pattern to find {% url ''namespace:name'' ... %}
FAULTY_URL_PATTERN = re.compile(r"{%\s*url\s+\'\'([a-zA-Z0-9_:]+)\'\'\s*([^%]*?)%}")

fixed_files = 0
fixed_tags = 0

print("Scanning for faulty URL tags...")

for root, dirs, files in os.walk(TEMPLATE_DIR):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            needs_fix = False
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all occurrences of the faulty pattern
                matches = FAULTY_URL_PATTERN.findall(content)
                
                if matches:
                    needs_fix = True
                    corrected_content = FAULTY_URL_PATTERN.sub(r"{% url '\1' \2%}", content)
                    fixed_tags_in_file = len(matches)
                    fixed_tags += fixed_tags_in_file
                    print(f"Found {fixed_tags_in_file} issue(s) in: {file_path}")

                    # Write the corrected content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(corrected_content)
                    fixed_files += 1

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if fixed_files > 0:
    print(f"\nCorrected {fixed_tags} faulty URL tags in {fixed_files} files.")
else:
    print("\nNo faulty URL tags found requiring correction.") 