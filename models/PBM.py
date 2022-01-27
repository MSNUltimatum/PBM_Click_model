from typing import List, NoReturn

from estimation.em_estimation import EMEstimation
from models.abstract_model import ClickModel
from parameters.abstract_parameter import ClickModelParameter, QueryDocumentAttr, RangeAttr
from utils.product_types import Session, Result


class PBMModel(ClickModel):
    def __init__(self):
        self.attractive_param: QueryDocumentAttr = QueryDocumentAttr(PBMAttractive)
        self.examination_param: RangeAttr = RangeAttr(PBMExamine)

    def train(self, training_dataset: List[Session]):
        return EMEstimation.train(self, training_dataset)

    def get_conditional_probability(self, session: Session):
        pass

    def get_full_probability(self, session: Session):
        pass


class PBMAttractive(ClickModelParameter):
    def update(self, result: Result, session_params) -> NoReturn:
        attr: float = session_params['attr'].value()
        exam: float = session_params['attr'].value()
        if result.is_clicked:
            self._numerator += 1
        else:
            self._numerator += (1 - exam) * attr / (1 - exam * attr)
        self._denominator += 1


class PBMExamine(ClickModelParameter):
    def update(self, result: Result, session_params) -> NoReturn:
        attr: float = session_params['attr'].value()
        exam: float = session_params['attr'].value()
        if result.is_clicked:
            self._numerator += 1
        else:
            self._numerator += (1 - attr) * exam / (1 - exam * attr)
        self._denominator += 1
