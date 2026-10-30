#!/usr/bin/env python3
"""predcheck - a small logic-coverage helper for students (Python 3, no dependencies).

It does two jobs for ONE predicate at a time:

1. `gen`   lists the test REQUIREMENTS of the predicate under PC, CC, GACC, CACC
           and RACC, and computes the smallest set of truth-value rows that
           satisfies RACC (and CACC).
2. `check` reads your concrete tests from a CSV file, works out the truth value of
           every clause for each test, and tells you which criteria your tests
           satisfy and which requirements are still missing.

Predicates may be written in Java or Python syntax:  && || !  or  and or not.

    python tools/predcheck.py gen   "express && (!member || weight > 5)"
    python tools/predcheck.py check "express && (!member || weight > 5)" my_tests.csv

CSV format: first line = variable names used in the predicate, then one row per
test. Booleans may be written true/false/T/F/1/0. A variable that is *derived
inside the program* (such as `fee` in D6) must be given as a column too: you
have to work out its value for each test.

Limits (be aware of them when you interpret the output)
  * Clauses are the maximal sub-expressions without logical operators. A
    negated clause (`!member`) is the clause `member`; the negation is part of
    the predicate structure.
  * The `gen` mode treats clauses as independent boolean variables. It does NOT
    know that two clauses may be coupled (for example `weight > 10` and
    `weight > 5`) or that some combinations are infeasible at a particular
    place in the program. Checking feasibility is YOUR job.
  * A clause that appears twice in the predicate with identical text is treated
    as one clause. Predicates with more than 8 clauses are refused.
"""
import ast
import csv
import itertools
import re
import sys


# ----------------------------------------------------------------- parsing
def to_python(expr):
    expr = expr.replace("&&", " and ").replace("||", " or ")
    expr = re.sub(r"!(?!=)", " not ", expr)
    expr = re.sub(r"\btrue\b", "True", expr)
    expr = re.sub(r"\bfalse\b", "False", expr)
    return expr.strip()


class Predicate:
    def __init__(self, text):
        self.text = text
        self.tree = ast.parse(to_python(text), mode="eval").body
        self.clauses = []          # source text of each clause, in order of appearance
        self._collect(self.tree)
        if len(self.clauses) > 8:
            raise SystemExit("predicate has more than 8 clauses; split it first")

    def _collect(self, node):
        if isinstance(node, ast.BoolOp):
            for v in node.values:
                self._collect(v)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            self._collect(node.operand)
        else:
            src = ast.unparse(node)
            if src not in self.clauses:
                self.clauses.append(src)

    def value(self, assignment, node=None):
        """Evaluate the predicate for {clause_text: bool} WITHOUT short-circuiting."""
        node = self.tree if node is None else node
        if isinstance(node, ast.BoolOp):
            vals = [self.value(assignment, v) for v in node.values]
            return all(vals) if isinstance(node.op, ast.And) else any(vals)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not self.value(assignment, node.operand)
        return assignment[ast.unparse(node)]


# ----------------------------------------------------------------- criteria
def all_rows(pred):
    n = len(pred.clauses)
    rows = []
    for bits in itertools.product([True, False], repeat=n):
        rows.append(bits)
    return rows


def flip(bits, i):
    return bits[:i] + (not bits[i],) + bits[i + 1:]


def pval(pred, bits):
    return pred.value(dict(zip(pred.clauses, bits)))


def determines(pred, bits, i):
    return pval(pred, bits) != pval(pred, flip(bits, i))


def racc_pairs(pred, i):
    out = []
    for bits in all_rows(pred):
        if bits[i] and determines(pred, bits, i):
            out.append((bits, flip(bits, i)))
    return out


def cacc_pairs(pred, i):
    out = []
    rows = all_rows(pred)
    for a in rows:
        if not a[i] or not determines(pred, a, i):
            continue
        for b in rows:
            if b[i] or not determines(pred, b, i):
                continue
            if pval(pred, a) != pval(pred, b):
                out.append((a, b))
    return out


def gacc_pairs(pred, i):
    t = [r for r in all_rows(pred) if r[i] and determines(pred, r, i)]
    f = [r for r in all_rows(pred) if (not r[i]) and determines(pred, r, i)]
    return [(a, b) for a in t for b in f]


def fmt(bits):
    return "".join("T" if b else "F" for b in bits)


def minimal_cover(pairs_per_clause):
    """Smallest set of rows containing one pair for every clause (exhaustive, small n)."""
    best = [None]
    options = [list(p) for p in pairs_per_clause]
    if any(not o for o in options):
        return None

    def rec(i, chosen):
        if best[0] is not None and len(chosen) >= len(best[0]):
            return
        if i == len(options):
            best[0] = set(chosen)
            return
        for a, b in options[i]:
            rec(i + 1, chosen | {a, b})

    rec(0, frozenset())
    return sorted(best[0], reverse=True) if best[0] else None


# ----------------------------------------------------------------- gen mode
def gen(pred):
    n = len(pred.clauses)
    print("Predicate : %s" % pred.text)
    print("Clauses   : " + "   ".join("c%d = %s" % (k + 1, c) for k, c in enumerate(pred.clauses)))
    print("Rows are written as truth values of (%s)\n" % ", ".join("c%d" % (k + 1) for k in range(n)))

    rows = all_rows(pred)
    print("Truth table (%d rows)" % len(rows))
    for r in rows:
        print("  %s  ->  %s" % (fmt(r), "T" if pval(pred, r) else "F"))

    print("\nPC   needs the predicate true once and false once.")
    print("     true rows : %s" % " ".join(fmt(r) for r in rows if pval(pred, r)))
    print("     false rows: %s" % " ".join(fmt(r) for r in rows if not pval(pred, r)))

    print("\nCC   needs every clause true once and false once (2 rows can suffice, e.g. %s and %s)."
          % (fmt(tuple([True] * n)), fmt(tuple([False] * n))))

    racc_all, cacc_all = [], []
    for i, c in enumerate(pred.clauses):
        rp, cp, gp = racc_pairs(pred, i), cacc_pairs(pred, i), gacc_pairs(pred, i)
        racc_all.append(rp)
        cacc_all.append(cp)
        print("\nClause c%d = %s" % (i + 1, c))
        print("  GACC pairs (c determines p in both rows): %d" % len(gp))
        print("  CACC pairs (also p differs; other clauses may differ): %d"
              % len(cp))
        print("     " + ("  ".join("%s/%s" % (fmt(a), fmt(b)) for a, b in cp) or "none -> clause is never active"))
        print("  RACC pairs (other clauses identical): %d" % len(rp))
        print("     " + ("  ".join("%s/%s" % (fmt(a), fmt(b)) for a, b in rp) or "none -> clause is never active"))

    for name, allp in (("RACC", racc_all), ("CACC", cacc_all)):
        m = minimal_cover(allp)
        if m is None:
            print("\n%s cannot be satisfied: some clause is never active." % name)
        else:
            print("\nSmallest %s row set: %d rows -> %s" % (name, len(m), " ".join(fmt(r) for r in m)))
    print("\nReminder: this is the abstract view. Decide yourself which rows are feasible in the program"
          " and what concrete inputs produce them.")


# --------------------------------------------------------------- check mode
def parse_bool_or_number(s):
    s = s.strip()
    low = s.lower()
    if low in ("true", "t"):
        return True
    if low in ("false", "f"):
        return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def clause_vector(pred, env):
    bits = []
    for node_src in pred.clauses:
        bits.append(bool(eval(to_python(node_src), {"__builtins__": {}}, dict(env))))
    return tuple(bits)


def check(pred, path):
    with open(path, newline="") as fh:
        rdr = csv.DictReader(fh)
        tests = [{k.strip(): parse_bool_or_number(v) for k, v in row.items()} for row in rdr]
    print("Predicate : %s" % pred.text)
    print("Clauses   : " + "   ".join("c%d = %s" % (k + 1, c) for k, c in enumerate(pred.clauses)))
    print()
    vecs = []
    for n, env in enumerate(tests, 1):
        try:
            v = clause_vector(pred, env)
        except NameError as exc:
            raise SystemExit("test %d: %s - add that variable as a CSV column" % (n, exc))
        vecs.append(v)
        print("  test %-2d %-40s clauses=%s  predicate=%s" % (
            n, ", ".join("%s=%s" % kv for kv in env.items()), fmt(v), "T" if pval(pred, v) else "F"))

    pvals = [pval(pred, v) for v in vecs]
    n = len(pred.clauses)
    rowset = set(vecs)
    print()
    ok = lambda b: "satisfied" if b else "NOT satisfied"
    print("PC  : %s" % ok(any(pvals) and not all(pvals)))
    cc_missing = []
    for i, c in enumerate(pred.clauses):
        for val in (True, False):
            if not any(v[i] == val for v in vecs):
                cc_missing.append("c%d(%s)=%s" % (i + 1, c, "T" if val else "F"))
    print("CC  : %s%s" % (ok(not cc_missing), ("   missing: " + ", ".join(cc_missing)) if cc_missing else ""))

    for name, fn in (("GACC", None), ("CACC", cacc_pairs), ("RACC", racc_pairs)):
        missing = []
        for i, c in enumerate(pred.clauses):
            if name == "GACC":
                t = any(v[i] and determines(pred, v, i) for v in rowset)
                f = any((not v[i]) and determines(pred, v, i) for v in rowset)
                good = t and f
            else:
                good = any(a in rowset and b in rowset for a, b in fn(pred, i))
            if not good:
                missing.append("c%d(%s)" % (i + 1, c))
        print("%-4s: %s%s" % (name, ok(not missing),
                              ("   no pair found for: " + ", ".join(missing)) if missing else ""))
    dup = len(vecs) - len(rowset)
    if dup:
        print("\nNote: %d test(s) repeat a clause-value row already produced by another test."
              " Are they redundant for this predicate?" % dup)


def main(argv):
    if len(argv) < 2 or argv[0] not in ("gen", "check"):
        print(__doc__)
        raise SystemExit(1)
    pred = Predicate(argv[1])
    if argv[0] == "gen":
        gen(pred)
    else:
        if len(argv) < 3:
            raise SystemExit("check needs a CSV file")
        check(pred, argv[2])


if __name__ == "__main__":
    main(sys.argv[1:])
