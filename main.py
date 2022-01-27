from typing import List

from utils.YandexDataParser import YandexDataParser
import os

from utils.util import Session

if __name__ == '__main__':
    path: str = os.path.join('data', 'YandexRelPredChallenge')
    parsed_sessions: List[Session] = YandexDataParser.parse(path)
