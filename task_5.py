import os
import re

def serialize_xml(obj, root="root"):
    if isinstance(obj, dict):
        return f"<{root}>" + ''.join(serialize_xml(v, k) if isinstance(v,(dict,list)) else f"<{k}>{v}</{k}>" for k,v in obj.items()) + f"</{root}>"
    if isinstance(obj, list):
        return ''.join(serialize_xml(i, root) for i in obj)
    return f"<{root}>{obj}</{root}>"

def validate_xml(xml):
    lines, stack = xml.splitlines(), []
    for i, line in enumerate(lines, 1):
        for match in re.finditer(r'</?([^>\s]+)[^>]*>', line):
            tag = match.group(1)
            if match.group()[1] == '/':  # закрывающий
                if not stack or stack[-1] != tag:
                    return f"Ошибка на строке {i}: несоответствие тега </{tag}>"
                stack.pop()
            elif not match.group().endswith('/>'):  # открывающий
                stack.append(tag)
    return f"Ошибка: не закрыты {stack}" if stack else "OK"

def deserialize_xml(xml):
    xml = re.sub(r'>\s+<', '><', xml.strip())
    def parse(pos=0):
        res, key, val = {}, None, []
        i = pos
        while i < len(xml):
            if xml[i] == '<':
                end = xml.find('>', i)
                tag = xml[i+1:end]
                if tag.startswith('/'):
                    return (val[0] if len(val)==1 and not isinstance(val[0], dict) else val, end+1) if key else (res, end+1)
                if tag.endswith('/'):
                    tag = tag[:-1].strip()
                    (res if key is None else val).append({tag: None} if key is not None else ({tag: None},))
                else:
                    tag_name = tag.split()[0]
                    if key is None:
                        res[tag_name], i = parse(end+1)
                        return res, i
                    child, i = parse(end+1)
                    val.append(child)
                continue
            if key is not None and xml[i] != '<':
                text_end = xml.find('<', i)
                if text_end == -1: break
                text = xml[i:text_end].strip()
                if text: val.append(text)
                i = text_end
                continue
            i += 1
        return res, i
    return parse()[0] if xml else {}

# Тест
data = {"user":{"name":"Alex","age":23,"skills":["Python","Git"]}}
xml = serialize_xml(data).replace("><",">\n<")
print(xml)
print("Валидация:", validate_xml(xml))
print("Десериализация:", deserialize_xml(xml))