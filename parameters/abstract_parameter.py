from abc import abstractmethod
from collections import defaultdict
from typing import Dict, NoReturn, Tuple, List, DefaultDict, Callable, Any

from utils.product_types import Result


class ClickModelParameter(object):
    def __init__(self, numerator: float = 1, denominator: float = 2):
        self.MIN_PROB = 0.0001
        self._numerator: float = numerator
        self._denominator: float = denominator

    def value(self) -> float:
        return min(self._numerator / self._denominator, 1 - self.MIN_PROB)

    def update(self, result: Result, session_params) -> NoReturn:
        raise NotImplemented


class SessionParamsContainer(object):
    def __init__(self):
        self.session_params: DefaultDict[int, Dict[str, ClickModelParameter]] = defaultdict(lambda: dict())

    def append(self, elem: Dict[int, Dict[str, ClickModelParameter]]):
        self.session_params.update(elem)

    def get_at_rank(self, rank: int) -> Dict[str, ClickModelParameter]:
        return self.session_params[rank]

    def update_at_rank(self, rank: int, result: Result, original_params):
        for _, param in self.get_at_rank(rank).items():
            param.update(result, original_params.get_at_rank(rank))


class QueryDocumentAttr(object):
    def __init__(self, cls):
        self.target_class = cls
        self._attrs: DefaultDict[str, DefaultDict[str, cls]] = defaultdict(
            lambda: defaultdict(lambda: self.target_class()))

    def get_attr_for_query(self, query: str, document: str):
        return self._attrs[query][document]


class RangeAttr(object):
    def __init__(self, cls):
        self.MAX_RANGE = 10
        self.target_class = cls
        self._attrs: List[cls] = [cls() for _ in range(self.MAX_RANGE)]

    def get_attr_for_rank(self, rank: int):
        if rank > self.MAX_RANGE:
            raise IndexError(f"Invalid range. {rank} > {self.MAX_RANGE}.")
        return self._attrs[rank]
