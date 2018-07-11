import unittest
import numpy as np
from pyrcv.vote import Election


class TestVote(unittest.TestCase):

    def test_vote_per_candidate_ids(self):

        election = Election(
            choices=["A", "B", "C", "D"])

        election.vote([2, 1, 3])
        election.vote([2, 0, 3])
        election.vote([0, 1, 2])
        election.vote([0, 2, 1])
        election.vote([2, 1, 2])

        self.assertEquals(election.tally(), 'C')

    def test_init(self):

        election = Election(
            choices=["candiate_a", "candidate_b", "candidate_c", "chandidate_d"])

        # Vote per dicts
        election.vote({'candidate_a': 2, 'candidate_d': 1})
        election.vote({'candidate_a': 2, 'candidate_c': 1})

        # Vote per lists
        election.vote(['candidate_c', 'candidate_a'])

        # Vote per candidate ids
        election.vote([3, 1, 4, 2])
        election.vote([1, 3, 2])  # means a, c, b

        self.assertEquals(election.tally(), 'candidate_a')

        # Counting again yields again the winner
        self.assertEquals(election.tally(), 'candidate_a')


class TestCounts(unittest.TestCase):

    def setUp(self):

        self.election = Election(
            candidates=["A", "B", "C", "D"])

        self.votes = [
            [2, 1, 3],
            [2, 0, 3],
            [0, 1, 2],
            [0, 2, 1],
            [2, 1, 3],
        ]

    def test_eliminate_candidate(self):

        np.testing.assert_array_equal(
            self.election._eliminate_candidate(self.votes, 'C'),
            [
                [1, 3],
                [0, 3],
                [0, 1],
                [0, 1],
                [1, 3],
            ])

    def test_count_first_ranked(self):

        frequencies = self.election._count_first_ranked(self.votes)

        self.assertEqual(type(frequencies), dict)

        self.assertIn('A', frequencies)
        self.assertIn('B', frequencies)
        self.assertIn('C', frequencies)
        self.assertIn('D', frequencies)

        self.assertEqual(frequencies['A'], 2)
        self.assertEqual(frequencies['B'], 0)
        self.assertEqual(frequencies['C'], 3)
        self.assertEqual(frequencies['D'], 0)

    def test_has_winner(self):

        self.assertFalse(self.election._has_winner(
            {
                'A': 10,
                'B': 2,
                'C': 10,
                'D': 3
            }))

        self.assertTrue(self.election._has_winner(
            {
                'A': 11,
                'B': 2,
                'C': 10,
                'D': 3
            }))

    def test_get_winner(self):

        winner = self.election._get_winner(
            {
                'A': 11,
                'B': 2,
                'C': 10,
                'D': 3
            })

        self.assertEqual('A', winner)

        with self.assertRaises(Exception):
            self.election._get_winner(
                {
                    'A': 10,
                    'B': 2,
                    'C': 10,
                    'D': 3
                })
