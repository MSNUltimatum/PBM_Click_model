from typing import List, NoReturn, Dict

from estimation.em_estimation import EMEstimation
from models.abstract_model import ClickModel
from parameters.abstract_parameter import ClickModelParameter, QueryDocumentAttr, RangeAttr, SessionParamsContainer, \
    ParamContainer
from utils.product_types import Session, Result


class PBMModel(ClickModel):
    def __init__(self):
        self.attractive_param: QueryDocumentAttr = QueryDocumentAttr(PBMAttractive)
        self.examination_param: RangeAttr = RangeAttr(PBMExamine)

    def train(self, training_dataset: List[Session]):
        return EMEstimation().train(self, training_dataset)

    def get_conditional_probability(self, session: Session):
        pass

    def get_full_probability(self, session: Session) -> List[float]:
        session_params: SessionParamsContainer = self.get_session_parameters(session)
        click_probs = [0.0] * 10

        for rank, session_param in session_params.session_params.items():
            attr = session_param['attr'].value()
            exam = session_param['exam'].value()

            click_prob = attr * exam
            click_probs[rank] = click_prob

        return click_probs

    def get_session_parameters(self, session: Session) -> SessionParamsContainer:
        session_params: SessionParamsContainer = SessionParamsContainer()
        for rank, web_result in enumerate(session.search_results):
            attr_param: PBMAttractive = self.attractive_param.get_attr_for_query(session.query, web_result.result_id)
            examine_param: PBMExamine = self.examination_param.get_attr_for_rank(rank)
            session_params.append({rank: dict(attr=attr_param, exam=examine_param)})
        return session_params

    def params(self) -> Dict[str, ParamContainer]:
        return dict(attr=self.attractive_param, exam=self.examination_param)

    def set_params(self, params: Dict[str, ParamContainer]):
        self.attractive_param = params.get('attr', self.attractive_param)
        self.examination_param = params.get('exam', self.examination_param)


class PBMAttractive(ClickModelParameter):
    def update(self, result: Result, session_params: Dict[str, ClickModelParameter]) -> NoReturn:
        attr: float = session_params['attr'].value()
        exam: float = session_params['exam'].value()
        if result.is_clicked:
            self._numerator += 1
        else:
            self._numerator += (1 - exam) * attr / (1 - exam * attr)
        self._denominator += 1


class PBMExamine(ClickModelParameter):
    def update(self, result: Result, session_params: Dict[str, ClickModelParameter]) -> NoReturn:
        attr: float = session_params['attr'].value()
        exam: float = session_params['exam'].value()
        if result.is_clicked:
            self._numerator += 1
        else:
            self._numerator += (1 - attr) * exam / (1 - exam * attr)
        self._denominator += 1
