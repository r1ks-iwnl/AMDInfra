from pathlib import Path
import sys

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.parser.coverage_parser import parse_file, parse_coverpoints

LOGS = Path(__file__).resolve().parents[2] / "logs"


def test_overall_83_5():
    report = parse_file(LOGS / "83_50_overall_FCOV.txt")
    assert report["overall_coverage"] == 83.5


def test_overall_96_25():
    report = parse_file(LOGS / "96_25_overall_FCOV.txt")
    assert report["overall_coverage"] == 96.25


def test_total_bins_is_29_and_misses_are_correct():
    report = parse_file(LOGS / "78_5_overall_FCOV.txt")
    total_bins = sum(len(coverpoint["bins"]) for coverpoint in report["coverpoints"])
    total_misses = sum(not bin_entry["hit"] for coverpoint in report["coverpoints"] for bin_entry in coverpoint["bins"])

    assert total_bins == 29
    assert total_misses == 12


def test_known_bin_cp_vec_3_has_expected_hits():
    report = parse_file(LOGS / "78_5_overall_FCOV.txt")
    cp_vec = next(coverpoint for coverpoint in report["coverpoints"] if coverpoint["name"] == "cp_vec")
    known_bin = next(bin_entry for bin_entry in cp_vec["bins"] if bin_entry["name"] == "vec[ 3]")

    assert known_bin["hits"] == 0
    assert known_bin["hit"] is False
    assert known_bin["value"] == "0011"


def test_parse_coverpoints_raises_on_inconsistent_bin_status():
    malformed_log = """[2026-06-15 10:41:11 UTC]
==== PASSED ==== checks=12

=========== Functional Coverage ===========
 cp_vec    :  37.50%
 OVERALL   :  78.50%

 cp_vec bins  (in3in2in1in0):
   vec[ 0]  0000 : hits=0           HIT
===========================================
"""

    with pytest.raises(ValueError, match="Inconsistent bin status"):
        parse_coverpoints(malformed_log)
