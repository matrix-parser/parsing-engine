from CachedOCR import OCR
import re


words = []


def select_query(query):
    m = re.match(
        "select (.*) from (.*) as (.*) where (.*)",
        query,
    )
    if not m:
        return
    groups = m.groups()
    exec_query = f"def query():\n\tglobal {groups[0]}\n\t{groups[0]} = [{groups[2]} for {groups[2]} in {groups[1]} if {groups[3]}]\nquery()"
    execute(exec_query)
    return None


def export_query(query):
    m = re.match(
        "export (.*) as (.*)",
        query,
    )
    if m:
        groups = m.groups()
        exec_query = f"def query():\n\tglobal output\n\toutput['{groups[1]}'] = [word.text for word in {groups[0]}]\nquery()"
        execute(exec_query)
        return None


def end_query(string):
    if string == "end":
        execute(
            "import json\nwith open('output.json', 'w+') as file:\n\tfile.write(json.dumps(output))"
        )
        return


def set_query(string):
    m = re.match(
        "set (.*)",
        string,
    )
    if not m:
        return
    groups = m.groups()
    exec_query = (
        f"def query():\n\tglobal {groups[0].split()[0]}\n\t{groups[0]}\nquery()"
    )
    execute(exec_query)
    return


queries = [
    {"keyword": "select", "function": select_query},
    {"keyword": "export", "function": export_query},
    {"keyword": "set", "function": set_query},
    {"keyword": "end", "function": end_query},
]


def set_pdf(pdf_file_path):
    global words

    ocr = OCR(pdf_file_path)
    words = ocr.get_words()


def execute(string):
    exec(string)


def decode(string):
    keyword = string.split()[0]
    for query in queries:
        if query["keyword"] == keyword:
            return query["function"](string)
    return None


def query(query):
    exec_query = f"def query():\n\tglobal output\n\ttry: print(output)\n\texcept: output = dict()\nquery()"
    execute(exec_query)
    decode(query)
