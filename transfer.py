import json
import re

def parse_vrml(lines):
    def parse_node(lines, indent_level=0):
        node = {}
        current_indent = "  " * indent_level
        key = None
        value = None
        while lines:
            line = lines.pop(0).strip()
            if not line or line.startswith("#"):
                continue
            if "{" in line:
                key = line.split("{")[0].strip()
                node[key] = parse_node(lines, indent_level + 1)
            elif "}" in line:
                break
            elif "[" in line:
                key = line.split("[")[0].strip()
                node[key] = parse_node(lines, indent_level + 1)
            elif "]" in line:
                break
            else:
                parts = re.split(r'\s+', line, 1)
                if len(parts) == 2:
                    key, value = parts
                    node[key] = value
                else:
                    key = parts[0]
                    node[key] = None
        return node

    lines = lines.splitlines()
    return parse_node(lines)

def wbt_to_json(wbt_file_path, json_file_path):
    
    with open(wbt_file_path, 'r', encoding='utf-8') as file:
        wbt_content = file.read()

    
    parsed_data = parse_vrml(wbt_content)

   
    json_data = json.dumps(parsed_data, indent=2)

    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


wbt_file_path = 'fluid.wbt'  
json_file_path = 'fluid.json'  

wbt_to_json(wbt_file_path, json_file_path)