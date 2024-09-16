import os
from functions import * #TODO select only necessary functions
from classes import TextSummary
import collections

#TODO make Command line argument
regenerate_cache = True
add_to_cache = True

#TODO Dry these paths, make relative, eventually move to a JSON file
vault = "/Users/joachimpfefferkorn/Obsidian/Main_Vault"
daily_notes_aggregated = "/Users/joachimpfefferkorn/Obsidian/Main_Vault/daily_notes.md"
footer_path = "/Users/joachimpfefferkorn/repos/daily_note_organizer/footer.md"
cache_folder = "/Users/joachimpfefferkorn/repos/daily_note_organizer/cache"


#INIT
years = []
months = []

empty_tag = "$empty_note_summary$"

with open(footer_path, 'r') as footer_file:
    footer = footer_file.read() #TODO update footer

if not regenerate_cache:
    print("💾 Reading in existing cache")
    with open(f"{cache_folder}/summarized_note_cache.txt", 'w') as summarized_note_cache: #TODO pickle or JSON?
        unordered_note_summaries = summarized_note_cache.read()
else:
    print("🦎 Regenerating entire cache")
    unordered_note_summaries = {}

for note in os.listdir(vault): #TODO test this edge case
    if is_daily_note(note) and note not in unordered_note_summaries:
        print(f"🧩 Adding empty entry for {note} (these will be summarized later)")
        unordered_note_summaries[note] = empty_tag
note_summaries = collections.OrderedDict(sorted(unordered_note_summaries.items()))
print("📚 Note summary dictionary sorted:")

iterator = 0
for note, summary in note_summaries.items():
    iterator += 1
    print(f"\n🦕 Checking note {iterator} out of {len(note_summaries)}")
    if summary == empty_tag:
        print(f"🧙 creating note summary for {note}")
        note_summaries[note] = create_note_summary(f"{vault}/{note}")
    else:
        print("🕶️ Note summary already present")
    print("📑", note)
    print("📝 ", summary)

if regenerate_cache or add_to_cache:
    print("💿 Saving cache")
    summarized_note_cache = note_summaries






# with open(daily_notes_aggregated, 'w') as obsidian_note:
#     #TODO now this sorts through 
#     for sorted_note in daily_notes: 
#         if sorted_note[0:4] not in years:
#             print(f"🗓️ Adding {sorted_note[0:4]}")
#             obsidian_note.write("# {year}\n".format(year = sorted_note[0:4]))
#             years.append(sorted_note[0:4])
#         if sorted_note[0:7] not in months:
#             month = month_writer(sorted_note)
#             print(f"Adding {month}")
#             obsidian_note.write("## {month}\n".format(month = month))
#             months.append(sorted_note[0:7])

#         note_link = "[[{note_link}]]".format(note_link = sorted_note[:-3])
#         note_path = os.path.join(vault, sorted_note)
#         print("📝 Note Added: ", note_link)

#         note_summary = create_note_summary(note_path)
#         print("📖 Summarization Result: ",)
#         print(note_summary)

#         obsidian_note.write(note_link)
#         obsidian_note.write("\n")
#         obsidian_note.write(note_summary)
#         obsidian_note.write("\n")

#         #TODO don't repeat this generation unless prompted to (as in the case of a better model)
#     obsidian_note.write(footer)

#     #NOTE backed up in time machine at 7:21, sync turned off at 8:02 PM on sept 10