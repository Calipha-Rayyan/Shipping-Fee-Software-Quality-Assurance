#!/usr/bin/env bash
# Compile the program and your JUnit suites, then print the fault-detection matrix.
#   ./run.sh                 compile + matrix for all suites
#   ./run.sh --details       also list the failing tests
#   ./run.sh NodeCoverageTest EdgeCoverageTest   only these suites
#
# Needs JDK 11+ and two jars in ./lib (download once, see README.md):
#   lib/junit-4.13.2.jar   lib/hamcrest-core-1.3.jar
set -euo pipefail
cd "$(dirname "$0")"
CP_LIBS="lib/junit-4.13.2.jar:lib/hamcrest-core-1.3.jar"
rm -rf out && mkdir -p out/classes out/test
javac -g -d out/classes src/main/java/shipping/*.java
javac -g -d out/test -cp "out/classes:$CP_LIBS" src/test/java/shipping/*.java
java -cp "out/classes:out/test:$CP_LIBS" shipping.RunMatrix "$@"
