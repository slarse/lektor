# Report for assignment 3

## Project

Name: Lektor

URL: https://github.com/lektor/lektor

Lektor is a static website generator. It builds out an entire project from
static files into many individual HTML pages and has a built-in admin UI and
minimal desktop app.

## Onboarding experience

It was easy to build and test the project. The README contains a link to an
installation guide which states what Lektor depends on and how you install it.
After installing those requirements, we could just start a virtual environment
and run pip to install all dependencies needed for testing. After doing this,
all tests passed on our systems.

Lektor seems to be a project with big room for improvement in terms of test
coverage and documentation, but there are no open issues requesting
refactoring. Thus, we will *sadly* have to pick a different project for the
next assignment.

## Complexity

1. What are your results for the ten most complex functions? (If ranking
is not easily possible: ten complex functions)?
   * Did all tools/methods get the same result?
   * Are the results clear?
2. Are the functions just complex, or also long?
3. What is the purpose of the functions?
4. Are exceptions taken into account in the given measurements?
5. Is the documentation clear w.r.t. all the possible outcomes?

## Coverage

### Tools

For coverage measurements, we used the excellent
[`Coverage.py`](https://github.com/nedbat/coveragepy). It is very simple to use
and integrates well with pretty much any Python project. The documentation is
[similarly excellent](https://coverage.readthedocs.io/en/coverage-4.3.4/index.html).
To run our test suite normally, we issue the following command:

```bash
$ pytest tests
```
To run with `Coverage` (and branch coverage), it changes to this:

```bash
$ coverage run --branch --source=lektor -m pytest tests
```
The `--source=lektor` part tells `Coverage` to only trace the `lektor` package.
We were a little bit puzzled at first, because no coverage is actually emitted
by this command alone, you have to run `coverage report` afterwards to get the
results. Had we bothered to spend a couple of minutes reading the
[Quick start](https://coverage.readthedocs.io/en/v4.5.x/#quick-start), that
would not have been a problem, as it shows the correct command.

```bash
$ coverage report -m
```

The `-m` is for _missing_.  This gives a detailed report of missing statements
and branches. The somewhat annoying thing is that it does not seem to be
possible to show _only_ branch coverage. As branch coverage subsumes statement
coverage, there really is little need to show both, and the output from `report`
is fairly unreadable. There is however a way to generate a HTML report with easy
to read coverage metrics.

```bash
$ coverage html
```
The document will show the source code, and will highlight unreached statements
with red, and partially covered branching statements (i.e. one out of two
decisions made) with yellow. Everything that is fully covere lacks highlighting.

There is also a plugin for `pytest` (the test runner we use) called
[`pytest-cov`](https://github.com/pytest-dev/pytest-cov) that runs `Coverage`
automatically. It doesn't feature the most detailed output from the `report`
command (with missing statements/branches), but that information is all but
unreadable anyway. It shows coverage as a percentage and can generate the
HTML report, which is fully sufficient. Usage with `pytest-cov` looks like this:

```bash
$ pytest tests --cov lektor --cov-branch --cov-report html
```
This will generate the HTML report. Overall, it is very easy to integrate
coverage tools in a Python build environment. Part of an HTML report is shown
in the next section, when discussing our own tool.

### DYI

Show a patch that show the instrumented code in main (or the unit
test setup), and the ten methods where branch coverage is measured.

The patch is probably too long to be copied here, so please add
the git command that is used to obtain the patch instead:

git diff ...

What kinds of constructs does your tool support, and how accurate is
its output?

### Evaluation

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

## Refactoring

Plan for refactoring complex code:

Carried out refactoring (optional)

git diff ...

## Effort spent

For each team member, how much time was spent in

1. plenary discussions/meetings;

2. discussions within parts of the group;

3. reading documentation;

4. configuration;

5. analyzing code/output;

6. writing documentation;

7. writing code;

8. running code?

## Overall experience

What are your main take-aways from this project? What did you learn?

Is there something special you want to mention here?
