import markdown
import re
from bs4 import BeautifulSoup
#from transformers import pipeline, AutoTokenizer

def md_to_plaintext(md):
    html = markdown.markdown(md)
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))
    cleaned = ""
    for char in text:
        if char != "[" and char != "]":
            cleaned += char
    return cleaned

def summarize(md_path, summarizer, tokenizer):

    with open(md_path, 'r') as NOTE:
        text = md_to_plaintext(NOTE.read())
        tokens = tokenizer(text)
        num_tokens = len(tokens['input_ids'])

    return summarizer(text, max_length=num_tokens, min_length=30, do_sample=False)

def summarize_string(text, summarizer, tokenizer):
    tokens = tokenizer(text)
    num_tokens = len(tokens['input_ids'])

    return summarizer(text, max_length=num_tokens, min_length=30, do_sample=False)

def month_writer(daily_note: str) -> str:
    month_num = daily_note[5:7]
    match month_num:
        case "01":
            return "January"
        case "02":
            return "February"
        case "03":
            return "March"
        case "04":
            return "April"
        case "05":
            return "May"
        case "06":
            return "June"
        case "07":
            return "July"
        case "08":
            return "August"
        case "09":
            return "September"
        case "10":
            return "October"
        case "11":
            return "November"
        case "12":
            return "December"
        case _ :
            return "Error defining month"