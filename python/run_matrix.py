#!/usr/bin/env python3
"""Fault-detection matrix.

Runs each of your test suites (tests/test_<criterion>.py) against the correct
program and against the ten faulty versions f01..f10, and prints which faults
each suite detects ("killed").

    python run_matrix.py                # all suites
    python run_matrix.py nc ec          # only the suites you name
    python run_matrix.py --details      # also list the failing test names

A suite is trusted only if it PASSES on the reference program. If it fails there
the matrix marks the column INVALID: fix your expected values first.
"""
import os
import subprocess
import sys

SUITES = ["nc", "ec", "pc", "cc", "cacc", "racc", "extra"]
FAULTS = ["f%02d" % i for i in range(1, 11)]


def run_suite(suite, target):
    env = dict(os.environ, TARGET=target)
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_" + suite],
        env=env, capture_output=True, text=True,
    )
    failed = [l.split()[1] for l in proc.stderr.splitlines()
              if l.startswith(("FAIL:", "ERROR:"))]
    return proc.returncode, failed, proc.stderr


def main(argv):
    details = "--details" in argv
    chosen = [a for a in argv if not a.startswith("--")] or SUITES
    table, ntests, valid = {}, {}, {}
    for s in chosen:
        rc, failed, err = run_suite(s, "ref")
        valid[s] = rc == 0
        ran = [l for l in err.splitlines() if l.startswith("Ran ")]
        ntests[s] = int(ran[0].split()[1]) if ran else 0
        if not valid[s]:
            print("!! Suite %-5s FAILS on the reference program -> INVALID (%s)"
                  % (s, ", ".join(failed) or "import error"))
            if not failed:
                print(err[-600:])
            continue
        for f in FAULTS:
            rc, failed, _ = run_suite(s, f)
            table[(s, f)] = failed if rc != 0 else None

    col = 7
    print()
    print("%-6s" % "fault" + "".join(("%-" + str(col) + "s") % s for s in chosen))
    print("%-6s" % "tests" + "".join(("%-" + str(col) + "d") % ntests[s] for s in chosen))
    print("-" * (6 + col * len(chosen)))
    for f in FAULTS:
        row = "%-6s" % f
        for s in chosen:
            if not valid[s]:
                cell = "n/a"
            else:
                cell = "KILL" if table[(s, f)] is not None else "."
            row += ("%-" + str(col) + "s") % cell
        print(row)
    print("-" * (6 + col * len(chosen)))
    print("%-6s" % "killed" + "".join(
        ("%-" + str(col) + "s") % (sum(1 for f in FAULTS if valid[s] and table[(s, f)] is not None)
                                    if valid[s] else "n/a") for s in chosen))
    survivors = [f for f in FAULTS
                 if all((not valid[s]) or table[(s, f)] is None for s in chosen)]
    print("\nSurvived every valid suite:", ", ".join(survivors) or "none")
    if details:
        print()
        for s in chosen:
            if not valid[s]:
                continue
            for f in FAULTS:
                if table[(s, f)]:
                    print("  %-5s kills %s via: %s" % (s, f, ", ".join(table[(s, f)])))


if __name__ == "__main__":
    main(sys.argv[1:])
