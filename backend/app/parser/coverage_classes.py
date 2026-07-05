import re
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum, auto



RE_RUN_DATE = re.compile(r"^\[(?P<run_date>[^\]]+)\]")
RE_RESULT = re.compile(r"====\s*(?P<result>PASSED|FAILED)\s*====\s*checks=(?P<checks>\d+)")
RE_OVERALL = re.compile(r"^\s*OVERALL\s*:\s*(?P<overall_coverage>[\d.]+)%\s*$")

RE_CPOINT = re.compile(r"^\s*(?P<name>\w+)\s*:\s*(?P<coverage>[\d.]+)%\s*$")
RE_CPOINT_BINS = re.compile(r"^\s*(?P<name>\w+)\b.*\bbins\b.*:\s*$")
RE_BIN_GENERIC = re.compile(
    r"^\s*(?P<name>.+?)\s*:\s*hits=(?P<hits>\d+)\s+"
    r"(?P<hit>\*\*\* MISS \*\*\*|HIT)\s*$")
RE_BIN_VEC = re.compile(
    r"^\s*(?P<name>vec\[\s*\d+\])\s+(?P<value>[01]{4})\s*:\s*hits=(?P<hits>\d+)"
    r"\s+(?P<hit>\*\*\* MISS \*\*\*|HIT)")


class State(Enum):
    BEFORE_COVERAGE = auto()
    IN_SUMMARY = auto()
    IN_BINS = auto()
    DONE = auto()

@dataclass()
class Coverpoint:
    name: str
    coverage: float
    bins: list = field(default_factory=list)

@dataclass
class Bin:
    name: str
    hits: int
    hit: bool
    value: str

@dataclass()
class CoverageReport:
    run_datetime: datetime
    result: str
    checks: int
    overall_coverage: float
    coverpoints: list
