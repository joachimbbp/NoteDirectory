from transformers import pipeline


def clean_md_line(md):
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
    max_input_length = 1024
    truncated_cleaned = cleaned[:max_input_length] #TODO make this somehow longer, or include salient parts, perhaps manual parsing

    max = min(int(len(truncated_cleaned) / 4), max_input_length)
    if max < 5:
        max = 5 #you can clean this code up tbh
        #INVESTIGATE You should consider increasing `max_length` or, better yet, setting `max_new_tokens`

    print(f"max: {max}, cleaned: {len(cleaned)}")

    #TODO Token indices sequence length is longer than the specified maximum sequence length for this model (1995 > 1024). Running this sequence through the model will result in indexing errors 
    summary = summarizer(truncated_cleaned, max_length=max, min_length=1, do_sample=False)
    return summary[0]['summary_text']