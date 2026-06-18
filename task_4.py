import os
import re


def serialize(obj, indent=0, level=0):
    sp = " " * indent if indent else ""
    nl = "\n" if indent else ""

    if obj is None: return "null"
    if isinstance(obj, bool): return "true" if obj else "false"
    if isinstance(obj, (int, float)): return str(obj)
    if isinstance(obj, str): return f'"{obj}"'

    if isinstance(obj, list):
        if not obj: return "[]"
        items = [serialize(i, indent, level + 1) for i in obj]
        if indent:
            inner = " " * (indent * (level + 1))
            end = " " * (indent * level)
            return f"[{nl}{inner}" + f",{nl}{inner}".join(items) + f"{nl}{end}]"
        return "[" + ",".join(items) + "]"

    if isinstance(obj, dict):
        if not obj: return "{}"
        pairs = [f'"{k}":{serialize(v, indent, level + 1)}' for k, v in obj.items()]
        if indent:
            inner = " " * (indent * (level + 1))
            end = " " * (indent * level)
            return f"{{{nl}{inner}" + f",{nl}{inner}".join(pairs) + f"{nl}{end}}}"
        return "{" + ",".join(pairs) + "}"


def validate(json_str):
    lines = json_str.splitlines()
    stack = []
    in_str = False

    for i, line in enumerate(lines, 1):
        for j, ch in enumerate(line, 1):
            if ch == '"' and (j == 1 or line[j - 2] != '\\'):
                in_str = not in_str
            if in_str: continue

            if ch in '{[':
                stack.append((ch, i))
            elif ch == '}':
                if not stack or stack[-1][0] != '{':
                    return False, f"Ошибка: лишняя '}}' на строке {i}"
                stack.pop()
            elif ch == ']':
                if not stack or stack[-1][0] != '[':
                    return False, f"Ошибка: лишняя ']' на строке {i}"
                stack.pop()

    if stack:
        return False, f"Ошибка: не закрыта '{stack[-1][0]}' на строке {stack[-1][1]}"

    try:
        eval(json_str.replace('true', 'True').replace('false', 'False').replace('null', 'None'), {"__builtins__": {}},
             {})
        return True, "OK"
    except:
        return False, "Ошибка синтаксиса"


def deserialize(json_str):
    return eval(json_str.replace('true', 'True').replace('false', 'False').replace('null', 'None'),
                {"__builtins__": {}}, {})


# Тест
if __name__ == "__main__":
    data = {"name": "Ivan", "age": 21, "skills": ["Python", "Git"], "active": True}

    json_str = serialize(data, indent=4)
    print(json_str)

    ok, msg = validate(json_str)
    print(f"\nВалидация: {msg}")

    # Проверка с ошибкой
    bad = '{"name":"Ivan","skills":["Python"]]}'
    ok, msg = validate(bad)
    print(f"Ошибка: {msg}")