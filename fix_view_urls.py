import os
import re

VIEWS_DIR = 'questionarios/views'
NS_PREFIX = 'questionarios:'
URL_PATTERN = re.compile(r"success_url\s*=\s*reverse_lazy\(['\"](?!questionarios:)([a-zA-Z_]+)['\"]")

fixed_files = 0
fixed_lines = 0

for root, dirs, files in os.walk(VIEWS_DIR):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Match success_url = reverse_lazy('url_name') pattern
            matches = URL_PATTERN.findall(content)
            if matches:
                corrected = URL_PATTERN.sub(r"success_url = reverse_lazy('" + NS_PREFIX + r"\1'", content)
                
                if corrected != content:
                    fixed_files += 1
                    fixed_lines += len(matches)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(corrected)
                    print(f'Fixed file: {file_path} ({len(matches)} URLs)')

print(f'Fixed {fixed_lines} URLs in {fixed_files} files.') 