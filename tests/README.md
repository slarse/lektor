# Running with the coveragetool plugin
To run the test suite with our homebrewn coveragetool, you need to set the
`COVTOOL_TRACE` environment variable to anything but the empty string.
If you have a look at the top of [`conftest.py`](conftest.py), you'll see why
this works. You should also ignore the tests in `tests/coveragetool`, as they
could interfere with the tracing (they shouldn't but they use the same global
tracing mechanics, so ignore just to be safe). This one-liner takes care of
everything:

```bash
$ export COVTOOL_TRACE=1; pytest tests/ --ignore=tests/coveragetool; unset COVTOOL_TRACE;
```

The files that are traced and functions that are displayed are hardcoded in
[`coveragetool/plugin.py`](../coveragetool/plugin.py). Note that the tool
currently only traces `if`, `while` and `for` statements. It also gets
really confused by conditions spread across multiple lines, so for maximum
non-confusion, edit any traced functions to have only single-line conditions.

You may need to install the project in editable mode again, so if this isn't
working, run `pip install -e .[test]` from the project root.
