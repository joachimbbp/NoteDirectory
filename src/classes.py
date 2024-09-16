from transformers import pipeline, AutoTokenizer
import torch

class TextSummary:
    def __init__(self, content):
        #AI
        self.model_name = "knkarthick/MEETING_SUMMARY"
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available GPT
        self.summarizer = pipeline("summarization", self.model_name, device=self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        #Text Content
        self.content = content
        self.tokens = self.tokenizer(content)
        self.num_tokens = len(self.tokens['input_ids']) #TODO there is a direct way to get these, slight hack for now
    def summarize_content(self):
        return self.summarizer(self.content, max_length=self.num_tokens, min_length=30, do_sample=False)[0]['summary_text']
    def clean_content(self):
        print("🧼 cleaning summarized note for markdown formatting")
        clean_summary = self.content
        replacement_table = {'[':'',']':'','#':'','`':'','*':'','-':'','$':''} #not sure if this is better than the naive way tbh
        for entry in replacement_table:
            clean_summary = clean_summary.replace(entry, replacement_table[entry])
        return clean_summary
    def summarize_and_clean(self):
        self.summarize_content() #possible code review needed
        return self.clean_content()