#! /bin/bash
#
# Shell script for running the test suite

TOOL="$1" # "coveragetool" or "Coverage"
WITH_NEW_TESTS="$2" # empty or non-empty

function usage() {
    echo "run_tests.sh <TOOL> [WITH_NEW_TESTS]"
}

if [ -z "$TOOL" ]; then
    usage
    exit 1
fi

CMD="pytest tests/ --ignore=tests/coveragetool"
if [ -z "$WITH_NEW_TESTS" ]; then
    CMD="$CMD --ignore=tests/newtests"
fi

if [ "$TOOL" = "coveragetool" ]; then
    export COVTOOL_TRACE=1
    eval "$CMD"
    unset COVTOOL_TRACE;
elif [ "$TOOL" = "Coverage" ]; then
    CMD="$CMD --cov lektor --cov-branch"
    eval "$CMD"
fi
