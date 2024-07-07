# 🤫 Prototype
Prototype of [🤫 from Huntinality 3: Hunts Upon A Time](https://www.huntinality.com/puzzles/puzzle_4). This may be useful for prototyping other [Funny Farm](https://devjoe.appspot.com/huntindex/keyword/funnyfarm)-style puzzles.

Inspired by [Collage](https://puzzles.mit.edu/2023/interestingthings.museum/puzzles/collage) from MIT Mystery Hunt 2023 ([prototype](https://github.com/alexirpan/collage-prototype)). Built using [vis.js](https://visjs.github.io/vis-network/docs/network/).


Much of the logic/code is puzzle-specific. 

# Requirements

- Python
  - `networkx`
  - `emoji`

# Usage Guide

## Solvers

Navigate to `puzzle_page/index.html`.

## Constructors

1. Modify `data/edges_sheet.txt` and `data/synonyms.txt`.
2. Run `make_graph.py`, which updates `puzzle_page/graph_data.js`.
