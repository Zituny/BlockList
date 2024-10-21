import requests
import datetime
import os
import pandas as pd
from pandas.errors import EmptyDataError
import shutil
from datetime import datetime
import pytz
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
with open('FromNextDNS.txt', 'r') as file:
    lines = file.readlines()
FromNextDNSBefore = len(lines)



url = os.getenv('NEXTDNSURL')
api_key = os.getenv('NEXTDNSAPIKEY')

headers = {
    "X-Api-Key": api_key
}



params = {
    "limit": 1000,
    "status": "blocked"
}
response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    logs = response.json()
    print("Domains retrieved successfully!")
    logs_data = logs['data']
    df = pd.json_normalize(logs_data)
    filtered_df = df[df['status'] == 'blocked']
    domain_values = filtered_df['domain']
    domain_values_unique = domain_values.drop_duplicates()
    domain_values_prepend = '||' + domain_values_unique + '^'
    with open("FromNextDNS.txt", "r") as FromNextDNS:
        old_content = FromNextDNS.read()
    with open("FromNextDNS.txt", "w") as FromNextDNS:
        for line in domain_values_prepend:
            FromNextDNS.write(line + '\n')
        FromNextDNS.write(old_content)
    print("Domains saved successfully!")
else:
    print(f"Failed to retrieve logs from NextDNS. Status code: {response.status_code}")
    print(response.text)
with open('FromNextDNS.txt', 'r') as file:
    lines = file.readlines()
unique_lines = list(set(lines))
unique_lines.sort()
with open('FromNextDNS.txt', 'w') as file:
    file.writelines(unique_lines)
with open('FromNextDNS.txt', 'r') as file:
    lines = file.readlines()
FromNextDNSAfter = len(lines)
Added = FromNextDNSAfter - FromNextDNSBefore
print(f"{Added} Domains added from NextDNS, {FromNextDNSAfter} Total Domains from NextDNS")
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
file_to_delete = 'BlockList.txt'
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted.")
else:
    print(f"{file_to_delete} does not exist.")
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
def download_file_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None
with open("lists.txt", "r") as file:
    urls = file.readlines()
urls = [url.strip() for url in urls]
combined_content = []
for url in urls:
    content = download_file_content(url)
    if content:
        combined_content.append(content)
combined_text = "\n".join(combined_content)
with open("BlockList.txt", "w") as output_file:
    output_file.write(combined_text)
num_lines = combined_text.count('\n') + 1
print(f"All lists downloaded with {num_lines} lines.")
def remove_duplicates(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    unique_lines = list(set(lines))
    deleted_count = len(lines) - len(unique_lines)  
    unique_lines.sort()
    with open(file_name, 'w') as file:
        file.writelines(unique_lines)
    print(f"Removed {deleted_count} duplicate lines. Total unique lines: {len(unique_lines)}")
    return deleted_count
line_count = 0
with open('BlockList.txt', 'r') as file:
    for line in file:
        line_count += 1
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
line_count = 0
with open('BlockList.txt', 'r') as file:
    for line in file:
        line_count += 1
print(f'BlockList.txt - Total = {line_count}')
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
with open('FromNextDNS.txt', 'r') as source_file:
    from_nextdns_lines = source_file.readlines()
with open('BlockList.txt', 'a') as target_file: 
    target_file.writelines(from_nextdns_lines)
line_count = 0
with open('BlockList.txt', 'r') as file:
    for line in file:
        line_count += 1
print(f'NextDNS Lines Added - Total = {line_count}')
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(f'Step 1 - Total = {line_count}')
with open('BlockList.txt', 'r') as file:
    lines = file.readlines()
deleted_count = 0
valid_lines = []
for line in lines:
    if line.startswith('||'):  
        valid_lines.append(line)  
    else:
        deleted_count += 1  
print(f"Deleted {deleted_count} lines that didn't start with '||'.")
with open('Blocklist1_startwell.txt', 'w') as file:
    file.writelines(valid_lines)
print("Cleaned blocklist saved to 'Blocklist1_startwell.txt'.")
line_count = 0
with open('Blocklist1_startwell.txt', 'r') as file:
    for line in file:
        line_count += 1  
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(f'Step 2 - Total = {line_count}')
remove_duplicates('Blocklist1_startwell.txt')
with open('Blocklist1_startwell.txt', 'r') as file:
    lines = file.readlines()
deleted_count = 0
valid_lines = []
deleted_lines = []  
for line in lines:
    stripped_line = line.strip()  
    if stripped_line.endswith('^'):  
        valid_lines.append(line)
    else:
        deleted_lines.append(stripped_line)  
        deleted_count += 1  
print(f"Deleted {deleted_count} lines that didn't end with '^'.")
with open('Blocklist2_containending.txt', 'w') as file:
    file.writelines(valid_lines)
print("Cleaned blocklist saved to 'Blocklist2_containending.txt'.")
print(f"Deleted lines logged to 'deleted_lines_log.txt'.")
line_count = len(valid_lines)  
print(f'Total lines in Blocklist2_containending.txt: {line_count}')
line_count = 0
with open('Blocklist2_containending.txt', 'r') as file:
    for line in file:
        line_count += 1
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(f'Step 3 - Total = {line_count}')
remove_duplicates('Blocklist2_containending.txt')
with open('Blocklist2_containending.txt', 'r') as file:
    lines = file.readlines()
deleted_count = 0
valid_lines = []
for line in lines:
    if line.count('^') == 1 and '/' not in line and '\\' not in line and '$' not in line and '?' not in line:
        valid_lines.append(line)  
    else:
        deleted_count += 1
print(f"Deleted {deleted_count} lines that contained more than one '^'.")
with open('Blocklist3_StratOkEndOk.txt', 'w') as file:
    file.writelines(valid_lines)
print("Cleaned blocklist saved to 'Blocklist3_StratOkEndOk.txt'.")
line_count = len(valid_lines)  
print(f'Total lines in Blocklist1_max_one_caret.txt: {line_count}')
line_count = 0
with open('Blocklist3_StratOkEndOk.txt', 'r') as file:
    for line in file:
        line_count += 1  
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(f'Step 4 - Total = {line_count}')
remove_duplicates('Blocklist3_StratOkEndOk.txt')
from publicsuffix2 import get_sld
from collections import defaultdict
def is_valid_format(line):
    """Checks if a line starts with '||' and ends with '^'."""
    trimmed_line = line.strip()  
    return trimmed_line.startswith('||') and trimmed_line.endswith('^')
with open('Blocklist3_StratOkEndOk.txt', 'r') as file:
    lines = file.readlines()
invalid_count = 0  
valid_lines = []
for line in lines:
    if is_valid_format(line):
        valid_lines.append(line)
    else:
        invalid_count += 1
        print(f"Invalid line: '{line.strip()}' (Length: {len(line.strip())})")  
print(f"Deleted {invalid_count} lines due to improper format.")
input_file = 'Blocklist3_StratOkEndOk.txt'
output_file = 'Blocklist4_StratOkEndOkNoWWW.txt'
fixed_count = 0
with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        if line.startswith('||www.'):
            fixed_line = line.replace('||www.', '||', 1)
            fixed_count += 1  
        else:
            fixed_line = line
        f_out.write(fixed_line)
print(f"Processed file saved as '{output_file}'")
print(f"Total lines fixed: {fixed_count}")
line_count = 0
with open('Blocklist4_StratOkEndOkNoWWW.txt', 'r') as file:
    for line in file:
        line_count += 1  
print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(f'Step 5 - Total = {line_count}')
remove_duplicates('Blocklist4_StratOkEndOkNoWWW.txt')
import tldextract
def process_domains(domains):
    base_domains = set()
    cleaned_domains = set()      
    for line in domains:
        domain = line.strip().lstrip("||").rstrip("^")
        extracted = tldextract.extract(domain)
        base_domain = f"{extracted.domain}.{extracted.suffix}"
        if base_domain not in base_domains:
            cleaned_domains.add(line.strip())
            if extracted.subdomain == "":
                base_domains.add(base_domain)
    return cleaned_domains
def clean_blocklist_sequential(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    cleaned_domains = process_domains(lines)
    with open("BlockList.txt", 'w') as f:
        for domain in sorted(cleaned_domains):
            f.write(f"{domain}\n")    
    print("Processing complete. Cleaned list saved.'")
clean_blocklist_sequential('Blocklist4_StratOkEndOkNoWWW.txt')
remove_duplicates('BlockList.txt')
file_to_delete = 'Blocklist1_startwell.txt'
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted.")
else:
    print(f"{file_to_delete} does not exist.")
file_to_delete = 'Blocklist2_containending.txt'
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted.")
else:
    print(f"{file_to_delete} does not exist.")
file_to_delete = 'Blocklist3_StratOkEndOk.txt'
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted.")
else:
    print(f"{file_to_delete} does not exist.")
file_to_delete = 'Blocklist4_StratOkEndOkNoWWW.txt'
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted.")
else:
    print(f"{file_to_delete} does not exist.")
file_name = "BlockList.txt"
israel_tz = pytz.timezone('Asia/Jerusalem')
date_time = datetime.now(israel_tz).strftime("%d%m%Y_%H%M%S")
with open(file_name, 'r') as file:
    line_count = sum(1 for line in file)
print(f"The file {file_name} contains {line_count} lines.")
lines_to_add = [
    "[Adblock Plus]",
    f"! Version: {date_time}",
    f"! Rules count: {line_count}",
    f"! Title: BlockList"
]
with open(file_name, 'r') as file:
    original_content = file.readlines()
with open(file_name, 'w') as file:
    for line in lines_to_add:
        file.write(line + '\n')
    file.writelines(original_content)
with open('BlockList.txt', 'r') as file:
    line_count = sum(1 for _ in file)
print(f"The file BlockList.txt contains {line_count} lines.")
with open('BlockList.txt', 'r') as file:
    line_count = sum(1 for _ in file)
log_file = "Log.txt"
new_line = f"{date_time} - Total: {line_count}\n"
with open(log_file, "r") as log:
    old_content = log.read()
with open(log_file, "w") as log:
    log.write(new_line + old_content)
