# pyrcv
Python library for ranked choice voting.

[![Build Status](https://travis-ci.org/windisch/pyrcv.svg?branch=master)](https://travis-ci.org/windisch/pyrcv)

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

# Vote, here, the numbers represents the place where the candidate
# stands on the candidate list (i.e., 2 stands for candidate_c) and
# the ordering of the numbers represents the ranking of the vote
election.vote([2, 1, 3])
election.vote([2, 0, 3]) 
election.vote([0, 1])
election.vote([0, 1])
election.vote([2, 1, 0, 3])

# Alternatively, vote per dict
election.vote(
   {
      'candidate_b': 1,
      'candidate_a': 2,
      'candidate_c': 3
   })

# Compute the winner
election.tally()
```
