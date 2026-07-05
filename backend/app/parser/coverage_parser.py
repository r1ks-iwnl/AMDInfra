import argparse
from dataclasses import asdict
import json
import sys
from datetime import datetime
from .coverage_classes import *

def parse_file(path):
    with open(path, "r") as file:
        content = file.read()

    header = parse_header(content)

    return CoverageReport(
        run_datetime=run_datetime(header["run_date"]),
        result=header["result"],
        checks=header["checks"],
        overall_coverage=header["overall_coverage"],
        coverpoints=parse_coverpoints(content)
    )


def run_datetime(run_date: str | None) -> str | None:
    if run_date is None:
        return None

    return datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S UTC")

    
def parse_header(text) -> dict:
    run_date = None
    result = None
    checks = None
    overall_coverage = None

    state = State.BEFORE_COVERAGE

    for line in text.splitlines():
        if(state == State.BEFORE_COVERAGE):
            match = RE_RUN_DATE.match(line)
            if(match):
                run_date = match.group("run_date")
                state = State.IN_SUMMARY

        if(state == State.IN_SUMMARY):
            match = RE_RESULT.match(line)
            if(match):
                result = match.group("result")
                checks = int(match.group("checks"))

            match = RE_OVERALL.match(line)
            if(match): 
                overall_coverage = float(match.group("overall_coverage"))

    state = State.DONE

    return {
        "run_date": run_date,
        "result": result,
        "checks": checks,
        "overall_coverage": overall_coverage
    }

def parse_coverpoints(text) -> list:
    coverpoints = []
    coverpoints_by_name = {}
    current_coverpoint = None

    state = State.IN_SUMMARY

    for line in text.splitlines():
        if(state == State.IN_SUMMARY):
            match = RE_CPOINT.match(line)
            if(match):
                name = match.group("name")
                coverage = float(match.group("coverage"))

                if(name == "OVERALL"):
                    state = State.IN_BINS
                    continue

                current_coverpoint = Coverpoint(name=name, coverage=coverage)
                coverpoints.append(current_coverpoint)
                coverpoints_by_name[name] = current_coverpoint

        elif(state == State.IN_BINS):
            bins_header = RE_CPOINT_BINS.match(line)
            if(bins_header):
                current_coverpoint = coverpoints_by_name.get(bins_header.group("name"))
                continue

            if(current_coverpoint is None):
                continue

            bin_regex = RE_BIN_VEC if current_coverpoint.name == "cp_vec" else RE_BIN_GENERIC
            match = bin_regex.match(line)
            if(match):
                name = match.group("name")
                hits = int(match.group("hits"))
                hit = match.group("hit") == "HIT"
                value = match.group("value") if "value" in match.groupdict() else None

                if ((hits > 0) != hit):
                    raise ValueError(f"Inconsistent bin status for {name}: hits={hits}, status={match.group('hit')}")

                current_coverpoint.bins.append(Bin(name=name,
                                                   hits=hits,
                                                   hit=hit,
                                                   value=value))

            if(line.strip() == "==========================================="):
                current_coverpoint = None
                state = State.DONE

    return coverpoints


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse a VCS functional coverage log and print JSON.")
    parser.add_argument("file", help="Path to the coverage log file as a string")
    args = parser.parse_args(argv)

    try:
        result = parse_file(args.file)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json_data = asdict(result)

    print(json.dumps(json_data, indent=2, default=str)) #default is currently fallback for datetime
    return 0


if __name__ == "__main__":
    raise SystemExit(main())