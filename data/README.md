# `edges_sheet.txt`
For every row in `edges_sheet.txt`, the first entry is connected to every other entry in the row.

### Category nodes
Categories are contained in the first section. 

Each row comes with 3 extra characters at the end, which indicate which letters to replace with a number on the visual label (e.g., ① instead of ●) for the puzzle's purposes.

# `synonyms.txt`

Like `edges_sheet.txt`, for every `synonyms.txt` row, the first entry is the primary entry, and every other entry will be treated as an alias for the primary by the puzzle. (A row with a single entry doesn't do anything.)

