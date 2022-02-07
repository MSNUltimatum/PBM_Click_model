import math
from typing import List

from models.abstract_model import ClickModel
from utils.product_types import Session


class PerplexityEvaluation(object):
    @staticmethod
    def evaluate(click_model: ClickModel, test_sessions: List[Session]):
        rank_position_perplexity: List[float] = [0.0] * 10

        for session in test_sessions:
            full_probs: List[float] = click_model.get_full_probability(session)

            for rank, prob in enumerate(full_probs):
                perplexity: float = prob if session.search_results[rank].is_clicked else (1 - prob)
                rank_position_perplexity[rank] += math.log(perplexity, 2)

        perplexity_at_rank = [2 ** (-x / len(test_sessions)) for x in rank_position_perplexity]
        perplexity = sum(perplexity_at_rank) / len(perplexity_at_rank)
        return perplexity, perplexity_at_rank
