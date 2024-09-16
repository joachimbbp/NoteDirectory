import os
from functions import *
from transformers import pipeline, AutoTokenizer
from classes import TextSummary

#PATHS
vault = "/Users/joachimpfefferkorn/Obsidian/Main_Vault"
daily_notes_aggregated = "/Users/joachimpfefferkorn/Obsidian/Main_Vault/daily_notes.md"
footer_path = "/Users/joachimpfefferkorn/repos/daily_note_organizer/footer.md"
#TODO Dry these paths

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


def create_note_summary(note_path):
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

        print("📝 Note Added: ", note_link)

        note_summary = create_note_summary(note_path)
        print("📖 Summarization Result: ",)
        print(note_summary)

        obsidian_note.write(note_link)
        obsidian_note.write("\n")
        obsidian_note.write(note_summary)
        obsidian_note.write("\n")

        #TODO don't repeat this generation unless prompted to (as in the case of a better model)
    obsidian_note.write(footer)

    #NOTE backed up in time machine at 7:21, sync turned off at 8:02 PM on sept 10