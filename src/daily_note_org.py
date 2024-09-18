import os
from functions import * #TODO select only necessary functions
from classes import TextSummary
import collections
import json

#Future CLI #TODO
regenerate_entire_cache = True
max_note_length = 5000
vault = "/Users/joachimpfefferkorn/Obsidian/Main_Vault"

#TODO Dry these paths, make relative
daily_notes_aggregated = "/Users/joachimpfefferkorn/Obsidian/Main_Vault/Daily Note Directory.md"
cache_folder = "/Users/joachimpfefferkorn/repos/NoteDirectory/cache"
cache_filenamename = "summarized_note_cache.json"
cache_path = f"{cache_folder}/{cache_filenamename}"

empty_tag = "$empty_note_summary$"



if not os.path.exists(cache_path):
    if not os.path.exists(cache_folder):
        print(f"🚧  {cache_folder} not present! Creating directory {cache_folder}")
        os.mkdir(cache_folder)
    print(f"🦺 {cache_filenamename} not present in {cache_folder}. Creating {cache_filenamename} and setting `regenerate_entire_cache` to true")
    c = open(cache_path, "x")
    c.close()
    regenerate_entire_cache = True

if not regenerate_entire_cache:
    print("💾 Reading in existing cache")
    with open(cache_path, 'r') as summarized_note_cache: #TODO pickle or JSON?
        unordered_note_summaries = json.loads(summarized_note_cache.read()) #MOVING LOGIC TO AFTER CACHE CREATION
else:
    print("🦎 Regenerating entire cache")
    unordered_note_summaries = {}

for note in os.listdir(vault): #TODO test this edge case
    if is_daily_note(note) and note not in unordered_note_summaries:
        print(f"🧩 Adding empty entry for {note} (these will be summarized later)")
        unordered_note_summaries[note] = empty_tag

note_summaries = collections.OrderedDict(sorted(unordered_note_summaries.items()))
print("📚 Note summary dictionary sorted")

iterator = 0
for note, summary in note_summaries.items():
    iterator += 1
    print(f"\n🦕 Checking note {iterator} out of {len(note_summaries)}")
    if summary == empty_tag:
        note_summary = create_note_summary(f"{vault}/{note}", max_note_length)
#        print("NOTE SUMMARY:, ", note_summary) #DEBUG, delete later
        note_summaries[note] = note_summary
    else:
        print("🕶️ Note summary already present")
    print("📑", note)
    print("📝 ", note_summaries[note])



print("💿 Saving cache")
json_cache = json.dumps(note_summaries, sort_keys=True, indent=4)
with open(cache_path, 'w') as summarized_note_cache:
    summarized_note_cache.write(json_cache)

print("💾 Reading in newly updated cache")
with open(cache_path, 'r') as summarized_note_cache:
    note_summary_dict = json.loads(summarized_note_cache.read())


years = []
months = []
print("🪨 Creating Obsidian note of all daily notes and their summaries")
with open(daily_notes_aggregated, 'w') as dailynote_file:
    for note in note_summary_dict:
        if note[0:4] not in years:
            print(f"🗓️ Adding {note[0:4]}")
            dailynote_file.write("# {year}\n".format(year = note[0:4]))
            years.append(note[0:4])
        if note[0:7] not in months:
            month = month_writer(note)
            print(f"Adding {month}")
            dailynote_file.write("## {month}\n".format(month = month))
            months.append(note[0:7])

        note_link = "[[{note_link}]]".format(note_link = note[:-3])
        note_path = os.path.join(vault, note)
        dailynote_file.write(note_link)
        print("📑 Note Added: ", note_link)
        dailynote_file.write("\n - ")
        dailynote_file.write(note_summary_dict[note])
        print(f"📝 Summary Added:\n{note_summary_dict[note]}")
        dailynote_file.write("\n")
print("🍾 Done!")