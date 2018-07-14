import unittest
import numpy as np
from pyrcv.vote import has_gaps
from pyrcv.vote import Election


class TestVote(unittest.TestCase):

    def test_vote_per_candidate_ids(self):

        election = Election(
            candidates=["A", "B", "C", "D"])

        election.vote([2, 1, 3])
        election.vote([2, 0, 3])
        election.vote([0, 1, 2])
        election.vote([0, 2, 1])
        election.vote([2, 1, 0])

        self.assertEquals(election.tally(), 'C')

    def test_tally(self):

        election = Election(
            candidates=["candidate_a", "candidate_b", "candidate_c", "candidate_d"])

        # Vote per dicts
        election.vote({'candidate_a': 1, 'candidate_d': 0})
        election.vote({'candidate_a': 1, 'candidate_c': 0})

        # Vote per lists
        # election.vote(['candidate_c', 'candidate_a'])

        # Vote per candidate ids
        election.vote([3, 1, 4, 2])
        election.vote([1, 3, 2])  # means a, c, b

        self.assertEquals(election.tally(), 'candidate_d')

        # Counting again yields again the winner
        self.assertEquals(election.tally(), 'candidate_d')

    def test_read_from_list(self):

        election = Election(
            candidates=["candidate_a", "candidate_b", "candidate_c", "candidate_d"])

        np.testing.assert_array_equal(
            [2, 0, 1, 3],
            election._read_vote_from_list([2, 0, 1, 3]))

        # No duplicate rankings
        with self.assertRaises(ValueError):
            election._read_vote_from_list([0, 1, 2, 1])

        # Candidate IDs have to match
        with self.assertRaises(ValueError):
            election._read_vote_from_list([3, 1, 2, 4, 0])

    def test_read_from_dict(self):

        election = Election(
            candidates=["candidate_a", "candidate_b", "candidate_c", "candidate_d"])

        np.testing.assert_array_equal(
            [3, 0],
            election._read_vote_from_dict({'candidate_a': 1, 'candidate_d': 0}))

        # No gaps
        with self.assertRaises(ValueError):
            election._read_vote_from_dict({'candidate_a': 0, 'candidate_c': 2})

        # Only known candidates
        with self.assertRaises(ValueError):
            election._read_vote_from_dict({'candidate_a': 1, 'candidate_ee': 0})

    def test_add_list_vote(self):

        election = Election(
            candidates=["candidate_a", "candidate_b", "candidate_c", "candidate_d"])

        # Vote per candidate ids
        election.vote([2, 0, 3, 1])
        election.vote([0, 2, 1])  # means a, c, b

        np.testing.assert_array_equal(
            election.votes,
            [
                [2, 0, 3, 1],
                [0, 2, 1]
            ])

    def test_remove_candidate_from_vote(self):

        election = Election(
            candidates=["candidate_a", "candidate_b", "candidate_c", "candidate_d"])

        self.assertListEqual(
            election._remove_candidate_from_vote([0, 1, 2, 3], 1),
            [0, 2, 3])

        self.assertListEqual(
            election._remove_candidate_from_vote([0, 1, 2, 3], 5),
            [0, 1, 2, 3])


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

    def test_get_candidate_to_eliminate(self):
        self.votes = [
            [2, 1, 3],
            [2, 0, 3],
            [0, 1, 2],
            [0, 2, 1],
            [2, 1, 3],
        ]

        counts = self.election._count_first_ranked(self.votes)
        lowest_candidates = self.election._get_candidates_to_eliminate(counts)
        np.testing.assert_array_equal(lowest_candidates, ['B', 'D'])

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

        # No absolute majority given
        self.assertFalse(self.election._has_winner(
            {
                'A': 11,
                'B': 2,
                'C': 10,
                'D': 3
            }))

        # No absolute majority given
        self.assertTrue(self.election._has_winner(
            {
                'A': 11,
                'B': 2,
                'C': 5,
                'D': 3
            }))

    def test_get_winner(self):

        winner = self.election._get_winner(
            {
                'A': 11,
                'B': 2,
                'C': 5,
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


class TestHelpers(unittest.TestCase):

    def test_has_gaps(self):
        self.assertTrue(has_gaps([1, 2]))
        self.assertTrue(has_gaps([0, 1, 3]))
        self.assertTrue(has_gaps([0, 1, 2, 10]))
        self.assertTrue(has_gaps([-1, 0, 1, 2]))

        self.assertFalse(has_gaps([0]))
        self.assertFalse(has_gaps([0, 1]))
        self.assertFalse(has_gaps([0, 1, 2, 3]))



