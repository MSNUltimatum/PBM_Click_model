from typing import List, Tuple, NoReturn


class Session(object):
    def __init__(self, query: str, session_id: str):
        self.query: str = query
        self.session_id: str = session_id
        self.search_results: List[Result] = []

    def get_result_ids(self) -> List[str]:
        return list(map(lambda result: result.result_id, self.search_results))

    def update_search_result(self, index: int, click: int) -> NoReturn:
        self.search_results[index].update(click)


class Result(object):
    def __init__(self, result_id: str, is_clicked: int = 0):
        self.result_id: str = result_id
        self.is_clicked: int = is_clicked

    def update(self, click: int) -> NoReturn:
        self.is_clicked: int = click


class Utils:
    @staticmethod
    def split_sessions(sessions: List[Session], training_length: float) -> Tuple[Session, Session]:
        training_session_length: int = int(len(sessions) * training_length)
        train_sessions: List[Session] = sessions[:training_session_length]
