from transformers import pipeline


def clean_md_line(md):
    print(f"clean md input: {md}")
    line = ""
    for char in md:
        if char.isalpha() or char == " ":
            line += char
    return line

def summarize(md_path):
    #just cleaning it now to debug
    summarizer = pipeline("summarization")
    print("CLEANING")
    cleaned = ""
    with open(md_path, 'r') as md:
        for line in md:
            cleaned += clean_md_line(line)
            cleaned += "\n"
    return summarizer(cleaned, max_length=50, min_length=30, do_sample=False) #quasi cargo cult code here