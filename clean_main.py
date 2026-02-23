#!/usr/bin/env python3
import re

# Read the file
with open('backend/main.py', 'rb') as f:
    content = f.read()

# Decode as UTF-8
content = content.decode('utf-8')

# Define specific emoji replacements
replacements = [
    ('✅', ''),
    ('❌', ''),
    ('⚠️', ''),
    ('🚀', ''),
    ('🔍', ''),
    ('📊', ''),
    ('🤖', ''),
    ('🎯', ''),
    ('⚡', ''),
    ('🟢', ''),
    ('🟡', ''),
    ('🔴', ''),
    ('🔬', ''),
    ('🔮', ''),
    ('📋', ''),
    ('🔔', ''),
    ('📈', ''),
    ('📉', ''),
    ('➖', ''),
    ('🚨', ''),
    ('⏳', ''),
    ('🗑️', ''),
    ('🛡️', ''),
    ('1️⃣', ''),
    ('2️⃣', ''),
    ('3️⃣', ''),
    ('4️⃣', ''),
    ('5️⃣', ''),
    ('6️⃣', ''),
    ('7️⃣', ''),
    ('8️⃣', ''),
    ('9️⃣', ''),
    ('ℹ️', ''),
    ('⚪', '')
]

# Apply replacements
for emoji, replacement in replacements:
    content = content.replace(emoji, replacement)

# Clean up extra spaces
content = re.sub(r'  +', ' ', content)
content = re.sub(r' \n', '\n', content)

# Write back
with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned backend/main.py")