# Daily Note Organizer
![directory note](readme_media/screenshot.png)
The Daily Note Organizer is a Python script designed to organize, aggregate, and summarize [Obsidian](https://obsidian.md/) daily notes in a single directory note (see screenshot above). 
This script currently works reasonably well, but does require some source code modifications (see *Usage* below). See the *Roadmap* section for planned functionality and interface improvements.

# Usage
**Disclaimer**: I recommend pausing obsidian sync before running this script and possibly keeping a local backup of all your obsidian files. I have not run into any catastrophic errors using this tool, but it is still in development and safety is not guaranteed.

**Instructions**
- Install and enter the [poetry environment](https://python-poetry.org/) for easy dependency management (optional)
    - `poetry install`
    - If in VSCode, select `venv:Poetry` as the Python interpreter in the command pallette 
- Navigate to `daily_note_org.py` and set the following:
    - If you need to regenerate your entire cache, set `regenerate_entire_cache` to True. Otherwise, keeping it as `False` should have the program only generate summaries for not-yet-summarized notes.
    - Set `max_note_length` to the maximum length of note you want summarized. I have set this to `5000` as I had some very large, somewhat nonsensical notes, that took very long to summarize. Feel free to tune to your liking.
    - `daily_notes_aggregated` should be a `daily_notes.md` file in your obsidian vault
    - `cache_folder` should be a directory where you would like to store your cache (I am keeping mine in my local repo)
- Run `daily_note_org.py` to generate your notes. This may take a while, but the debug print statements should give you a decent idea of where you are at.

# Roadmap
## Functionality
- [x] Add license
- [ ] Split large notes into sections based on their headers first, then along the lines if still necessary
- [ ] Use a separate model to summarize code blocks, integrate this sub-summary into the note summary in human language
- [ ] Cap maximum summary output length
- [ ] Fine-tune model
## Interface
- [ ] Set paths, `regenerate_entire_cache`, `max_note_length`, and any other tuneable variables as user-settable command line args
- [ ] Integrate into an Obsidian plugin
