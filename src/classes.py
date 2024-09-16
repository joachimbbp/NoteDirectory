from transformers import pipeline, AutoTokenizer
model_name = "knkarthick/MEETING_SUMMARY"
summarizer = pipeline("summarization", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

class Section:
    def __init__(self, content):
        self.content = content
        self.tokens = tokenizer(content)
        self.num_tokens = len(self.tokens['input_ids']) #TODO there is a direct way to get these, slight hack for now