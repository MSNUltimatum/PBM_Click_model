from typing import List

from Parsers.YandexDataParser import YandexDataParser
import os

from utils.Utils import Session

if __name__ == '__main__':
    path: str = os.path.join('Data', 'YandexRelPredChallenge')
    parsed_sessions: List[Session] = YandexDataParser.parse(path)
