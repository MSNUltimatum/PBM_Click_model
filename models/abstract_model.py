from abc import abstractmethod
from typing import List

from parameters.abstract_parameter import SessionParamsContainer
from utils.util import Session


class ClickModel(object):
    @abstractmethod
    def train(self, training_dataset: List[Session]):
        raise NotImplemented

    @abstractmethod
    def get_full_probability(self, session: Session):
        raise NotImplemented

    @abstractmethod
    def get_conditional_probability(self, session: Session):
        raise NotImplemented

    def get_session_parameters(self, session: Session) -> SessionParamsContainer:
        pass
