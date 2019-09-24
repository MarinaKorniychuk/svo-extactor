from typing import List

from mypy_extensions import TypedDict


class RawItem(TypedDict):
    url: str
    title: str
    text: str


class SVOTriple(TypedDict):
    name: str
    subject: str
    verb: str
    object: str
    url: str
    definition: str


RawData = List[RawItem]
SVOData = List[SVOTriple]
