import markdown
import re
from bs4 import BeautifulSoup
import numpy as np
from transformers import pipeline, AutoTokenizer
from classes import TextSummary
import os

# model_name = "knkarthick/MEETING_SUMMARY"
# summarizer = pipeline("summarization", model=model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)



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


def clean_md(md_content: str):
    clean_note = md_content
    clean_note = clean_note.replace('- [x]', 'Completed:').replace('- [ ]','To Do:')
    clean_note = clean_note.replace('[[', '').replace(']]','')
    clean_note = clean_note.replace('![[', 'Image file:')
    return clean_note


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




def prepare_note(md_path):
    with open(md_path, 'r') as note:
        md_content = note.read()
        cleaned_md = clean_md(md_content)
        return cleaned_md
    
def split(section: TextSummary, amount: int):
    lines = np.asarray(section.content.split("\n"), dtype=str)

    sub_arrays = np.array_split(lines, amount)

    sections = []
    #Make each sub array a string
    for array in sub_arrays:
        text = "\n".join(array)
    # then a section
    #add each section to a list
        sections.append(TextSummary(text))
    return sections

def biggest_section(sections):
    biggest_section = TextSummary("")
    for section in sections:
        if section.num_tokens > biggest_section.num_tokens:
            biggest_section = section
    return biggest_section

def summarize_sections(note_sections):
    summary = ""
    for i, section in enumerate(note_sections):
        print(f"📇 Summarizing section {i} out of {len(note_sections)}")
        summary += section.summarize_and_clean() + "\n"
        #summary += summarize_string(section.content, summarizer, tokenizer)['summary_text'] + "\n"
    return summary


def create_note_summary(note_path):
    print()
    prepared_note = prepare_note(str(note_path))
    note_sections = []
    og_section = TextSummary(prepared_note)
    split_amount = 1
    def recursive_split(input_section, split_amount):

        if input_section.num_tokens > input_section.tokenizer.model_max_length and split_amount < 99:
            split_amount += 1
            print(f"🐘 Original section must be split by {split_amount}! Section tokens: {input_section.num_tokens} Max model length: {input_section.tokenizer.model_max_length}")
            new_sections = split(og_section, split_amount)
            print(f"🪸 New sections updated with split subsections, 🔃 recursively split is recursing")
            for i, subsection in enumerate(new_sections):
                print(f"⚔️ Splitting subsection {i}")
                recursive_split(subsection, split_amount)
        else:
            print(f"🦋 Section is small enough!")
            print(f"🏄 Small enough section added to new_sections")
            note_sections.append(input_section)
            return 0

    recursive_split(og_section, split_amount)
    print(f"🏭 Summarizing {os.path.basename(note_path)}")
    summary = summarize_sections(note_sections)
    return summary

def is_daily_note(note):
    if note[:2] == "20" and note[4] == "-" and note[7] == "-":
        return True
    else:
        return False
    #You could code golf this to one line but I find this more readable