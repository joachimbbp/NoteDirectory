import markdown
import re
from bs4 import BeautifulSoup
import numpy as np
from transformers import pipeline, AutoTokenizer
from classes import Section

model_name = "knkarthick/MEETING_SUMMARY"
summarizer = pipeline("summarization", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)



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


def clean_md(md_content: str):
    clean_note = md_content
    clean_note = clean_note.replace('- [x]', 'Completed:').replace('- [ ]','To Do:')
    clean_note = clean_note.replace('[[', '').replace(']]','')
    clean_note = clean_note.replace('![[', 'Image file:')
    return clean_note

def prepare_note(md_path):
    with open(md_path, 'r') as note:
        md_content = note.read()
        cleaned_md = clean_md(md_content)
        return cleaned_md
    
def split(section: Section, amount: int):
    lines = np.asarray(section.content.split("\n"), dtype=str)

    sub_arrays = np.array_split(lines, amount)

    sections = []
    #Make each sub array a string
    for array in sub_arrays:
        text = "\n".join(array)
    # then a section
    #add each section to a list
        sections.append(Section(text))
    return sections

def biggest_section(sections):
    biggest_section = Section("")
    for section in sections:
        if section.num_tokens > biggest_section.num_tokens:
            biggest_section = section
    return biggest_section



    

def summarize_sections(note_sections):
    summary = ""
    for i, section in enumerate(note_sections):
        print(f"📇 Summarizing section {i}")
        summary += summarize_string(section.content, summarizer, tokenizer)[0]['summary_text'] + "\n"
        #summary += summarize_string(section.content, summarizer, tokenizer)['summary_text'] + "\n"
    return summary