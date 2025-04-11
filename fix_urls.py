import os
import re

TEMPLATE_DIR = 'questionarios/templates'
NS_PREFIX = 'questionarios:'
URL_PATTERN = re.compile(r'{%\s*url\s+[\'\"]((?!questionarios:)[a-zA-Z_]+)[\'\"]\s*%}')
URL_WITH_ARG_PATTERN = re.compile(r'{%\s*url\s+[\'\"]((?!questionarios:)[a-zA-Z_]+)[\'\"]([^%]+)%}')

fixed_files = 0

for root, dirs, files in os.walk(TEMPLATE_DIR):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace URLs without namespace
            corrected = URL_PATTERN.sub(r'{% url \'\'' + NS_PREFIX + r'\1\'' + r'\' %}', content)
            corrected = URL_WITH_ARG_PATTERN.sub(r'{% url \'\'' + NS_PREFIX + r'\1\'' + r'\2%}', corrected)
            
            if corrected != content:
                fixed_files += 1
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(corrected)
                print(f'Fixed file: {file_path}')

print(f'Fixed {fixed_files} files.') 