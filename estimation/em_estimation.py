import copy
from typing import List

from models.abstract_model import ClickModel
from parameters.abstract_parameter import SessionParamsContainer
from utils.product_types import Session


class EMEstimation(object):
    def __init__(self, iteration_count: int = 10):
        self.iteration_count: int = iteration_count

    def train(self, click_model: ClickModel, training_ds: List[Session]) -> ClickModel:
        if not training_ds or len(training_ds) == 0:
            return click_model

        original_model: ClickModel = copy.deepcopy(click_model)
        start_click_model: ClickModel = copy.deepcopy(click_model)

        for _ in range(self.iteration_count):
            training_model: ClickModel = copy.deepcopy(click_model)

            for session in training_ds:
                original_params: SessionParamsContainer = original_model.get_session_parameters(session)
                training_params: SessionParamsContainer = training_model.get_session_parameters(session)

                for rank, result in enumerate(session.search_results):
                    training_params.update_at_rank(rank, result, original_params)

            original_model. = training_params.params
