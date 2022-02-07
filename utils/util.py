from typing import List, Tuple, NoReturn

from utils.product_types import Session


class Utils(object):
    @staticmethod
    def split_sessions(sessions: List[Session], training_length: float) -> Tuple[List[Session], List[Session]]:
        training_session_length: int = int(len(sessions) * training_length)
        train_sessions: List[Session] = sessions[:training_session_length]
        work_sessions: List[Session] = sessions[training_session_length:]
        return train_sessions, work_sessions
