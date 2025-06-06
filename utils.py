import re

def parse_subject(email_text):
    subject_match = re.search(r"Subject:\s*(.+)", email_text)
    return subject_match.group(1).strip() if subject_match else ""

def parse_body(email_text):
    body_match = re.search(r"(Dear\s.+)", email_text, re.DOTALL)
    return body_match.group(1).strip() if body_match else ""
