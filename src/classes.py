from transformers import pipeline, AutoTokenizer

class TextSummary:
    def __init__(self, content):
        #AI
        self.model_name = "knkarthick/MEETING_SUMMARY"
        self.summarizer = pipeline("summarization", self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        #Text Content
        self.content = content
        self.tokens = self.tokenizer(content)
        self.num_tokens = len(self.tokens['input_ids']) #TODO there is a direct way to get these, slight hack for now
    def summarize_content(self):
        return self.summarizer(self.content, max_length=self.num_tokens, min_length=30, do_sample=False)[0]['summary_text']