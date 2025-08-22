# Conway's Game of Life

A Python implementation of Conway's cellular automaton.

## Rules

1. **Underpopulation**: Living cell with < 2 neighbors dies
2. **Survival**: Living cell with 2-3 neighbors survives
3. **Overpopulation**: Living cell with > 3 neighbors dies
4. **Reproduction**: Dead cell with exactly 3 neighbors becomes alive

## Usage

```bash
python game_of_life.py [options]
```

**Options:**
- `-b, --board_size`: Board size (default: 25)
- `-g, --generations`: Number of generations (default: 100)
- `-s, --saturation`: Initial density 0.0-1.0 (default: 0.4)
- `-f, --freq`: Time between generations (default: 0.2s)

**Examples:**
```bash
# Small fast simulation
uv run python game_of_life.py -b 20 -g 50 -s 0.2 -f 0.1

# Large sparse world
uv run python game_of_life.py -b 100 -g 500 -s 0.15
```

## TODO

- Create a function to add patterns in the pattern database export format

## Resources

- [Conway's Game of Life - Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [Pattern Database](https://conwaylife.com/wiki/Main_Page)