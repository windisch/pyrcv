# pyrcv
Python library for ranked choice voting. This is work in progress.

## Installation

Install with

```
pip install https://github.com/windisch/pyrcv.git
```

## Usage

```python
from pyrcv import Election

# Set up an election
election = Election(
    candidates=[
      "candidate_a", 
      "candidate_b", 
      "candidate_c",
      "candidate_d"])

# Vote
election.vote([2, 1, 3])
election.vote([2, 0, 3])
election.vote([0, 1, 2])
election.vote([0, 2, 1])
election.vote([2, 1, 0])

# Compute the winner
election.tally()
```
