from abc import abstractmethod
from collections import defaultdict
from typing import Dict, NoReturn, List, DefaultDict

from utils.product_types import Result


class ClickModelParameter(object):
    def __init__(self, numerator: float = 1, denominator: float = 2):
        self.MIN_PROB = 0.0001
        self._numerator: float = numerator
        self._denominator: float = denominator

    @abstractmethod
    def value(self) -> float:
        return min(self._numerator / float(self._denominator), 1 - self.MIN_PROB)

    @abstractmethod
    def update(self, result: Result, session_params) -> NoReturn:
        raise NotImplemented

    def __repr__(self):
        return str(self.value())


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


class ParamContainer(object):
    def __init__(self, cls):
        self.target_class = cls
        self._attrs = None


class QueryDocumentAttr(ParamContainer):
    def __init__(self, cls):
        super().__init__(cls)
        self._attrs: DefaultDict[str, DefaultDict[str, cls]] = defaultdict(
            lambda: defaultdict(lambda: self.target_class()))

    def get_attr_for_query(self, query: str, document: str):
        return self._attrs[query][document]

    def __repr__(self):
        repr_string = ""
        for query, d in self._attrs.items():
            for doc, attr in d.items():
                repr_string += f"{query} {doc} {attr}"
        return repr_string


class RangeAttr(ParamContainer):
    def __init__(self, cls):
        super().__init__(cls)
        self.MAX_RANGE = 10
        self._attrs: List[cls] = [cls() for _ in range(self.MAX_RANGE)]

    def get_attr_for_rank(self, rank: int):
        if rank > self.MAX_RANGE:
            raise IndexError(f"Invalid range. {rank} > {self.MAX_RANGE}.")
        return self._attrs[rank]

    def __str__(self):
        return '%s\n' % ' '.join([str(item) for item in self._attrs])

    def __repr__(self):
        return str(self._attrs)
