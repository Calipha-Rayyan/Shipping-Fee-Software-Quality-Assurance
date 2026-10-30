package shipping;

import java.util.ArrayList;
import java.util.List;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

/**
 * Fault-detection matrix (Java version of run_matrix.py).
 *
 * <p>Runs each of your JUnit suites against the correct program and against the faulty versions
 * f01..f10 and prints which faults each suite detects ("KILL"). A suite is trusted only if it
 * PASSES on the reference program; otherwise its column is marked n/a.
 *
 * <p>Usage: java -cp ... shipping.RunMatrix [--details] [NodeCoverageTest EdgeCoverageTest ...]
 */
public final class RunMatrix {

    private static final String[] DEFAULT_SUITES = {
        "NodeCoverageTest", "EdgeCoverageTest", "PredicateCoverageTest", "ClauseCoverageTest",
        "CorrelatedActiveClauseCoverageTest", "RestrictedActiveClauseCoverageTest", "ExtraTest"
    };
    private static final String[] SHORT = {"nc", "ec", "pc", "cc", "cacc", "racc", "extra"};

    private RunMatrix() {
    }

    public static void main(String[] args) throws Exception {
        boolean details = false;
        List<String> chosen = new ArrayList<>();
        for (String a : args) {
            if (a.equals("--details")) {
                details = true;
            } else {
                chosen.add(a);
            }
        }
        if (chosen.isEmpty()) {
            for (String s : DEFAULT_SUITES) {
                chosen.add(s);
            }
        }
        int n = chosen.size();
        int nf = 10;
        boolean[] valid = new boolean[n];
        int[] counts = new int[n];
        List<List<List<String>>> killedBy = new ArrayList<>();   // [suite][fault] -> failing tests
        for (int s = 0; s < n; s++) {
            Class<?> cls = Class.forName("shipping." + chosen.get(s));
            System.setProperty("target", "ref");
            Result ref = JUnitCore.runClasses(cls);
            counts[s] = ref.getRunCount();
            valid[s] = ref.wasSuccessful();
            List<List<String>> perFault = new ArrayList<>();
            if (!valid[s]) {
                System.out.println("!! " + chosen.get(s) + " FAILS on the reference program -> INVALID");
                for (Failure f : ref.getFailures()) {
                    System.out.println("     " + f.getTestHeader() + ": " + f.getMessage());
                }
            }
            for (int k = 1; k <= nf; k++) {
                List<String> failing = null;
                if (valid[s]) {
                    System.setProperty("target", String.format("f%02d", k));
                    Result r = JUnitCore.runClasses(cls);
                    if (!r.wasSuccessful()) {
                        failing = new ArrayList<>();
                        for (Failure f : r.getFailures()) {
                            failing.add(f.getDescription().getMethodName());
                        }
                    }
                }
                perFault.add(failing);
            }
            killedBy.add(perFault);
        }
        System.setProperty("target", "ref");

        StringBuilder sb = new StringBuilder("\n").append(String.format("%-6s", "fault"));
        for (int s = 0; s < n; s++) {
            sb.append(String.format("%-7s", s < SHORT.length && chosen.get(s).equals(DEFAULT_SUITES[s])
                    ? SHORT[s] : chosen.get(s).substring(0, Math.min(6, chosen.get(s).length()))));
        }
        sb.append('\n').append(String.format("%-6s", "tests"));
        for (int s = 0; s < n; s++) {
            sb.append(String.format("%-7d", counts[s]));
        }
        sb.append('\n');
        int[] killed = new int[n];
        List<String> survivors = new ArrayList<>();
        for (int k = 1; k <= nf; k++) {
            sb.append(String.format("%-6s", String.format("f%02d", k)));
            boolean any = false;
            for (int s = 0; s < n; s++) {
                String cell;
                if (!valid[s]) {
                    cell = "n/a";
                } else if (killedBy.get(s).get(k - 1) != null) {
                    cell = "KILL";
                    killed[s]++;
                    any = true;
                } else {
                    cell = ".";
                }
                sb.append(String.format("%-7s", cell));
            }
            if (!any) {
                survivors.add(String.format("f%02d", k));
            }
            sb.append('\n');
        }
        sb.append(String.format("%-6s", "killed"));
        for (int s = 0; s < n; s++) {
            sb.append(String.format("%-7s", valid[s] ? String.valueOf(killed[s]) : "n/a"));
        }
        System.out.println(sb);
        System.out.println("\nSurvived every valid suite: " + (survivors.isEmpty() ? "none" : String.join(", ", survivors)));
        if (details) {
            for (int s = 0; s < n; s++) {
                for (int k = 1; k <= nf; k++) {
                    List<String> f = valid[s] ? killedBy.get(s).get(k - 1) : null;
                    if (f != null) {
                        System.out.printf("  %-5s kills f%02d via: %s%n", SHORT[Math.min(s, SHORT.length - 1)], k, String.join(", ", f));
                    }
                }
            }
        }
    }
}
