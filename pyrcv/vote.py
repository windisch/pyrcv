import numpy as np
import logging
import operator


logger = logging.getLogger(__name__)


def has_gaps(l):
    """
    Checks if a list of numbers has gaps
    """

    l.sort()

    for i in range(len(l)):
        if i not in l:
            return True

    return False

class Election(object):

    def __init__(self, candidates):

        self.candidates = np.array(candidates)
        self.votes = []

        # TODO: Check uniqueness of candidates
        self.candidates_left = self.candidates

    def vote(self, ballot):
        """
        Adds the ballot of the voter to the election. Here, a ballot can either be a list or a dict

        List
        ----

        Here, the numbers represents the place where the candidate
        stands on the candidate list (i.e., 2 stands for candidate_c) and
        the ordering of the numbers represents the ranking of the vote

        Dict
        ----

        Here, the keys of the dict should represent the candidates name and the key its ranking.

        Args:
            ballot (list or dict): The vote
        """

        # Votes should be lists of candidate ids
        if type(ballot) == list:
            vote = self._read_vote_from_list(ballot)

        if type(ballot) == dict:
            vote = self._read_vote_from_dict(ballot)

        self.votes.append(vote)

    def _read_vote_from_list(self, ballot):
        ballot_set = set(ballot)
        if len(ballot_set) != len(ballot):
            raise ValueError('No duplicate namings allowed')

        if len(ballot) > len(self.candidates):
            raise ValueError('To much canidates')

        return ballot

    def _read_vote_from_dict(self, ballot):
        """

        Duplicate namings do not have to be checked as this is impossible in a dict
        """

        if len(set(ballot.values())) != len(ballot.keys()):
            raise ValueError('No duplicates allowed')

        if has_gaps(list(ballot.values())):
            raise ValueError('No gaps allowed')

        # Generate a list that sorts the candidate by their ranks
        candidates_by_rank = [k for k, v in sorted(ballot.items(), key=operator.itemgetter(1))]

        # Check candidates
        for c in candidates_by_rank:
            if c not in self.candidates:
                raise ValueError('Unkown candidates')

        # Convert to candidate ids
        return [self._get_candidate_id(c) for c in candidates_by_rank]

    def from_df(self):
        pass

    def _count_first_ranked(self, votes):

        # Compute first ranked
        first_ranks = np.array([vote[0] for vote in votes if len(vote) > 0])

        # Compute frequencies
        frequencies = dict()
        for candidate in self.candidates_left:
            frequencies[candidate] = np.sum(first_ranks == self._get_candidate_id(candidate))

        return frequencies

    def _has_winner(self, counts):

        values = np.fromiter(counts.values(), dtype=np.int)

        is_unique = np.sum(values == values.max()) == 1
        is_absolute = 2*values.max() > values.sum()

        return is_unique and is_absolute

    def _get_winner(self, counts):

        if not self._has_winner(counts):
            raise Exception('No winner of first rank votes')

        values = np.array([counts[candidate] for candidate in self.candidates_left], dtype=np.int)
        return self.candidates_left[values.argmax()]

    def _get_candidates_to_eliminate(self, counts, rule='all'):
        """
        Depending on the tie braking rule
        """

        # Extract the values based on the ordering
        values = np.array([counts[c] for c in self.candidates_left], dtype=np.int)

        return self.candidates_left[values == values.min()]

    def _get_candidate_id(self, candidate):
        """
        Args:
            candidate (string): Name of the candidate
        """

        return np.where(self.candidates == candidate)[0][0]

    def _remove_candidate_from_vote(self, vote, candidate_id):

        if candidate_id in vote:
            vote.remove(candidate_id)
        return vote

    def _eliminate_candidate(self, votes, candidate):

        candidate_id = self._get_candidate_id(candidate)

        logger.info('Eliminating {} (ID = {})'.format(candidate, candidate_id))

        return [
            self._remove_candidate_from_vote(vote, candidate_id) for vote in votes
        ]

    def tally(self):

        # Get copy of votes
        votes = self.votes

        winner = False

        for n_round in range(len(self.candidates)):
            logger.info('Starting round {}'.format(n_round))

            frequencies = self._count_first_ranked(votes)

            # Break infinity loop once a winner has been found
            if self._has_winner(frequencies):
                logger.info('Yeay, found winner!')
                winner = self._get_winner(frequencies)
                break
            # No winner
            candidates = self._get_candidates_to_eliminate(frequencies)

            for candidate in candidates:
                logger.info('Remove candidate {}'.format(candidate))
                votes = self._eliminate_candidate(votes, candidate)
                self.candidates_left = self.candidates_left[self.candidates_left != candidate] #remove(candidate)

        return winner
