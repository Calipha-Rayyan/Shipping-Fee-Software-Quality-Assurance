#!/usr/bin/env python3
"""bytecode_cfg - draw the control flow graph of a compiled Java method (Python 3, needs a JDK and Graphviz).

It runs `javap -c -l` on your compiled class, splits the bytecode of one method
into basic blocks, and writes a Graphviz DOT file. Each block is labelled with the
Java source lines it came from and its bytecode.

    python tools/bytecode_cfg.py out/classes shipping.ShippingRef fee > fee.dot
    dot -Tpng fee.dot -o fee.png            (or -Tsvg)

Compile with `javac -g` so that line numbers are present (run.sh does).

Why this tool is interesting for this course: the Java compiler turns `a || b` and
`a && b` into one conditional jump PER CLAUSE. In the bytecode graph you will
therefore see the clauses of a predicate as separate decision blocks, which is not
what the source-level CFG (a single diamond per predicate) shows.
"""
import re
import subprocess
import sys

INSN = re.compile(r"^\s+(\d+):\s+(\w+)\s*(.*)$")
LINE = re.compile(r"^\s+line\s+(\d+):\s+(\d+)\s*$")
RETURNS = {"return", "ireturn", "lreturn", "freturn", "dreturn", "areturn", "athrow"}


def javap(classpath, cls):
    out = subprocess.run(["javap", "-c", "-l", "-p", "-cp", classpath, cls],
                         capture_output=True, text=True, check=True).stdout
    return out.splitlines()


def method_section(lines, name):
    start = None
    for i, l in enumerate(lines):
        if re.match(r"^\s{2}\S.*\b%s\(" % re.escape(name), l):
            start = i
            break
    if start is None:
        raise SystemExit("method %r not found in class" % name)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^\s{2}\S", lines[j]):
            end = j
            break
    return lines[start:end]


def parse(section):
    insns, linemap = [], []
    for l in section:
        m = INSN.match(l)
        if m:
            insns.append((int(m.group(1)), m.group(2), m.group(3).strip()))
            continue
        m = LINE.match(l)
        if m:
            linemap.append((int(m.group(2)), int(m.group(1))))
    return insns, sorted(linemap)


def source_line(linemap, pc):
    best = None
    for start_pc, line in linemap:
        if start_pc <= pc:
            best = line
    return best


def build(insns):
    pcs = [p for p, _, _ in insns]
    leaders = {pcs[0]}
    for idx, (pc, op, arg) in enumerate(insns):
        nxt = pcs[idx + 1] if idx + 1 < len(pcs) else None
        if op.startswith("if") or op == "goto":
            leaders.add(int(arg.split()[0]))
            if nxt is not None:
                leaders.add(nxt)
        elif op in RETURNS and nxt is not None:
            leaders.add(nxt)
    leaders = sorted(leaders)
    blocks = {}
    for k, start in enumerate(leaders):
        stop = leaders[k + 1] if k + 1 < len(leaders) else float("inf")
        blocks[start] = [i for i in insns if start <= i[0] < stop]
    edges = []
    for start, body in blocks.items():
        pc, op, arg = body[-1]
        nxt_candidates = [s for s in leaders if s > start]
        nxt = nxt_candidates[0] if nxt_candidates else None
        if op == "goto":
            edges.append((start, int(arg.split()[0]), ""))
        elif op.startswith("if"):
            edges.append((start, int(arg.split()[0]), "jump"))
            if nxt is not None:
                edges.append((start, nxt, "fall-through"))
        elif op in RETURNS:
            pass
        elif nxt is not None:
            edges.append((start, nxt, ""))
    return blocks, edges


def to_dot(blocks, edges, linemap, title):
    out = ["digraph cfg {", '  label="%s"; labelloc=t; node [shape=box, fontname="Courier", fontsize=10];' % title]
    for start, body in blocks.items():
        lines = sorted({source_line(linemap, pc) for pc, _, _ in body if source_line(linemap, pc)})
        head = "B%d  (pc %d-%d)" % (start, body[0][0], body[-1][0])
        if lines:
            head += "\\nsource line%s %s" % ("s" if len(lines) > 1 else "", ", ".join(map(str, lines)))
        text = "\\l".join("%d: %s %s" % (pc, op, arg) for pc, op, arg in body) + "\\l"
        last = body[-1][1]
        style = ', style=filled, fillcolor="#ffd9d0"' if last.startswith("if") else (
            ', style=filled, fillcolor="#d6f5d6"' if last in RETURNS else "")
        out.append('  B%d [label="%s\\n%s"%s];' % (start, head, text, style))
    for a, b, lab in edges:
        out.append('  B%d -> B%d%s;' % (a, b, ' [label="%s"]' % lab if lab else ""))
    out.append("}")
    return "\n".join(out)


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    classpath, cls, method = argv
    section = method_section(javap(classpath, cls), method)
    insns, linemap = parse(section)
    blocks, edges = build(insns)
    print(to_dot(blocks, edges, linemap, "%s.%s" % (cls, method)))


if __name__ == "__main__":
    main(sys.argv[1:])
