import copy
from typing import List

from models.abstract_model import ClickModel
from utils.product_types import Session


class EMEstimation(object):
    def __init__(self, iteration_count: int = 10):
        self.iteration_count: int = iteration_count

    def train(self, click_model: ClickModel, training_ds: List[Session]) -> ClickModel:
        if not training_ds or len(training_ds) == 0:
            return click_model

        start_model: ClickModel = copy.deepcopy(click_model)
        start_click_model: ClickModel = copy.deepcopy(click_model)

        for _ in self.iteration_count:
            training_model: ClickModel = copy.deepcopy(click_model)

            for session in training_ds:

                for rank, result in enumerate(session.search_results):
