from typing import List

from evaluation.evaluation import PerplexityEvaluation
from models.PBM import PBMModel
from utils.YandexDataParser import YandexDataParser
from utils.product_types import Session
from utils.util import Utils

if __name__ == '__main__':
    sessions: List[Session] = YandexDataParser.parse('data/YandexRelPredChallenge')
    train_session, test_session = Utils.split_sessions(sessions, 0.75)
    pbm: PBMModel = PBMModel()
    train_model: PBMModel = pbm.train(train_session)
    zipped_result = zip(train_model.get_full_probability(test_session[0]), zip(test_session[0].search_results, range(
        len(test_session[0].search_results))))
    print('\n'.join(map(lambda x: f"{x[0]} | {str(x[1][0])} |  {str(x[1][1])}", sorted(zipped_result, key=lambda x: -x[0]))))
