# LeetCode

Personal archive of LeetCode problems I've solved, organized by topic, with notes for review.

## Structure

```
leetcode/
├── arrays/
├── dp/
├── graphs/
├── trees/
├── two-pointers/
├── sliding-window/
├── backtracking/
├── linked-list/
├── stacks-queues/
├── binary-search/
├── greedy/
└── heaps/
```

Each problem lives in its own folder: `<topic>/<number>-<slug>/` containing `solution.py` and `README.md`.

## Index

| # | Problem | Difficulty | Topic | Solution |
|---|---------|-----------|-------|----------|
<!-- add a row per problem, e.g.: -->
<!-- | 1 | Two Sum | Easy | Array, Hash Map | [link](arrays/0001-two-sum) | -->

## Adding a new problem

```bash
./new_problem.sh <number> <slug> <topic> <difficulty>
# example:
./new_problem.sh 1 two-sum arrays Easy
```

This scaffolds the folder, `solution.py`, and a `README.md` from the template, and prints the index row to paste above.
