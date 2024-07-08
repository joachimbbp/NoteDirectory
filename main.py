import os
vault = "/Users/joachimpfefferkorn/Obsidian/Main Vault"
daily_notes_aggregated = "/Users/joachimpfefferkorn/Obsidian/Main Vault/daily_notes.md"
daily_notes = []
years = []
months = []

# daily notes look like this: 2023-10-17.md
for note in os.listdir(vault):
    if note[:2] == "20" and note[4] == "-" and note[7] == "-":
        daily_notes.append(note)
daily_notes.sort()
print(daily_notes)

with open(daily_notes_aggregated, 'w') as obsidian_note:
    for sorted_note in daily_notes:
        note_link = "[[{note_link}]]".format(note_link = sorted_note[:-3])
        print("note link: ", note_link)
        obsidian_note.write(note_link)
        obsidian_note.write("\n")