## How To ...

---

### Run tests

within `aoc_23_solutions` directory:

```bash
❯ pytest tests/day_1.py
❯ pytest -s tests/day_2.py::DayTwoTests
❯ pytest -s tests/day_*
```

---

### Run puzzles

within `aoc_23_solutions` directory:

```bash
❯ python run_puzzle.py 2
```

---

### Install as a package

```bash
# ensure you are in the correct place to install
❯ pwd
advent-of-code/advent-of-code-2023/

# install as a package
❯ pip install -e .

# to run puzzles
❯ aoc_23_run_puzzle
```