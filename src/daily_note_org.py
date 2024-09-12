import os
from functions import summarize, month_writer
from transformers import pipeline, AutoTokenizer


#PATHS
vault = "/Users/joachimpfefferkorn/Obsidian/Main_Vault"
daily_notes_aggregated = "/Users/joachimpfefferkorn/Obsidian/Main_Vault/daily_notes.md"
footer_path = "/Users/joachimpfefferkorn/repos/daily_note_organizer/footer.md"
#TODO Dry these paths

#AI STUFF
model_name = "knkarthick/MEETING_SUMMARY"
summarizer = pipeline("summarization", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#INIT
daily_notes = []
years = []
months = []
with open(footer_path, 'r') as footer_file:
    footer = footer_file.read()

for note in os.listdir(vault):
    if note[:2] == "20" and note[4] == "-" and note[7] == "-":
        daily_notes.append(note)
daily_notes.sort()
print(daily_notes)

with open(daily_notes_aggregated, 'w') as obsidian_note:
    for sorted_note in daily_notes: 
        if sorted_note[0:4] not in years:
            obsidian_note.write("# {year}\n".format(year = sorted_note[0:4]))
            years.append(sorted_note[0:4])
        if sorted_note[0:7] not in months:
            obsidian_note.write("## {month}\n".format(month = month_writer(sorted_note)))
            months.append(sorted_note[0:7])

        note_link = "[[{note_link}]]".format(note_link = sorted_note[:-3])

        note_path = os.path.join(vault, sorted_note)

        print("note added: ", note_link)

        note_summary = summarize(note_path, summarizer, tokenizer)[0]['summary_text']
        print("summarization result: ", summarize(note_path, summarizer, tokenizer))
        print(note_summary)

        obsidian_note.write(note_link)
        obsidian_note.write("\n")
        obsidian_note.write(note_summary)#TODO here you put the summary
        obsidian_note.write("\n")

        #TODO don't repeat this generation unless prompted to (as in the case of a better model)
    obsidian_note.write(footer)

    #NOTE backed up in time machine at 7:21, sync turned off at 8:02 PM on sept 10