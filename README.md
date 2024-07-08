# Daily Note Organizer
Readme from chatgpt

## Overview
The Daily Note Organizer is a Python script designed to organize and aggregate daily notes stored in markdown files within an Obsidian vault. It sorts notes by year and month, creating a structured overview in a single markdown file.

## Features
- **Automatic Sorting**: Sorts all daily notes by year and month.
- **Aggregation**: Creates a single markdown file that aggregates links to all daily notes, organized by year and month.
- **Easy Navigation**: Enhances the ability to navigate through daily notes by providing a structured overview.

## Requirements
- Python 3.10 or higher (for match-case support)
- Access to an Obsidian vault with daily notes named in the `YYYY-MM-DD.md` format.

## Installation
1. Ensure Python 3.10 or higher is installed on your system.
2. Clone this repository or download the `main.py` script to your local machine.
3. Update the `vault` and `daily_notes_aggregated` variables in the script to point to your Obsidian vault and desired location for the aggregated markdown file, respectively.

## Usage
1. Navigate to the directory containing the `main.py` script.
2. Run the script using Python:
   ```shell
   python main.py