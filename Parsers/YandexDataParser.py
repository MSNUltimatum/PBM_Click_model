from typing import TextIO, List

from utils.Utils import Session, Result


class YandexDataParser:
    @staticmethod
    def parse(file_path: str) -> List[Session]:
        yandex_file: TextIO = open(file_path, 'r')
        sessions: List[Session] = []
        current_session: Session = None
        for line in yandex_file:
            split_line: List[str] = line.strip().split('\t')
            if len(split_line) >= 6 and split_line[2] == 'Q':
                session_id: str = split_line[0]
                query: str = split_line[3]
                results: List[str] = split_line[5:]
                current_session: Session = Session(query, session_id)

                for result in results:
                    search_result = Result(result)
                    current_session.search_results.append(search_result)
                sessions.append(current_session)
            elif len(split_line) == 4 and split_line[2] == 'C':
                session_id: str = split_line[0]
                if session_id == current_session.session_id:
                    clicked_result: str = split_line[3]
                    prev_session_results: List[str] = current_session.get_result_ids()
                    if clicked_result in prev_session_results:
                        result_index: int = prev_session_results.index(clicked_result)
                        current_session.update_search_result(result_index, 1)
            else:
                continue

        return sessions
