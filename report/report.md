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

We decided to go one step further than hard-coding, and actually implement a
real coverage tool. It works on some of the same principles as `Coverage`,
but is much less sophisticated. It is also a bit backwards. `Coverage` reports
which branches were _not_ taken, while or tool reports which branches _were_
taken. Given that information, it is easy for a human to figure out which
branches were not taken, but it required a lot of extra effort to automate it,
and we did not have the time to. The tool currently only considers `if`, `while`
and `for` statements, and is unable to cope with condition guards that are
spread across multiple lines ([explained below](#step-2.-stack-frame-tracing)).
It does work, however, which we think is pretty cool!  We call it
`coveragetool`, and you can
[find it here](https://github.com/slarse/lektor/tree/tooling/coveragetool).
Note that it is on the `tooling` branch of the repository! Now, let's get down
to how it works. Given a set of files to measure branch coverage in, the tool
does its thing in two distinct steps, as described in the following two
sections.

#### Step 1. Analyzing the abstract syntax tree
Before any tests are run, the tool compiles all files that should be traced
into abstract syntax trees. This is easy to do in Python using the
[`ast` module](https://docs.python.org/3/library/ast.html). The tree is then
traversed, and every conditional statement (that the tool knows is a conditional,
so `if`, `while` and `for`) has its line number recorded. This functionality
is implemented in the
[`coveragetool.branchfinder`](https://github.com/slarse/lektor/blob/tooling/coveragetool/branchfinder.py)
module.

#### Step 2. Stack frame tracing
The second step is performed during code execution. In CPython, each time a
function is called, a `call` event is dispatched to a callback function (if the
callback is set). This callback is known as the global trace function. If the
global trace function decides that the `call` event is worth tracing, it returns
a local trace function callback for that scope. The local trace function is then
called for several types of events, including each time a new line is executed.
Details can be found [here](https://docs.python.org/3/library/sys.html#sys.settrace).
We essentially use this to save the previously executed line on a per-stack
frame basis. Whenever we see that the preceding line was one of the recorded
lines from [Step 1](#step-1.-analyzing-the-abstract-syntax-tree), we map the
preceding line to the current line. Here's also the reason why `coveragetool`
can't handle guards that span multiple lines: the pre-processing of the AST
doesn't actually enter the guard, it just finds the conditional statement
itself. In the same spirit, compressing several conditionals onto a single line
(such as with a ternary) will get `coveragetool` confused. `Coverage` does
something similar with tracing, too, but its tracing is implemented in C (i.e.
is _much_ faster), and it performs no pre-processing with the AST, so we have no
idea of how it figures out which branches were not taken.  That's pretty much
all there is to it, the implementation can be found in
[`coveragetool.branchtracer`](https://github.com/slarse/lektor/blob/tooling/coveragetool/branchtracer.py).

#### Actually using `coveragetool`
To actually be able to use `coveragetool`, we implemented a small local `pytest`
plugin. It can be found in
[`coveragetool.plugin`](https://github.com/slarse/lektor/blob/tooling/coveragetool/plugin.py),
and usage instructions are available in
[`tests/README.md`](https://github.com/slarse/lektor/blob/tooling/tests/README.md).

#### Comparing `coveragetool` to `Coverage`
`Coverage` is much more sophisticated than our tool, and for example has no
issues dealing with multi-line conditional guards. However, when it comes to
single-line guards for `if`, `for` and `while`, performance is remarkably
similar. Below is small part of a `Coverage` HTML report for one of the complex
functions, modified to have only single-line guards.

![locate_executable coverage](images/locate_executable_cov.png)

And here is the (somewhat truncated) output from `coveragetool`, mapping
branch statement lines to which lines where jumped to:

```
 'locate_executable@utils.py': {280: {281,
                                      283},
                                285: {286},
                                288: {289,
                                      297},
                                290: {292},
                                292: {295},
                                293: set(),
                                297: {300},
                                301: {302},
                                302: {301,
                                      303},
                                303: {302,
                                      304}},
```

The outputs correspond, but are inverted, as `coveragetool` shows covered
branches, while `Coverage` does the opposite. For example, if we look at line
292, we can see that it is highlighted yellow, and that line 293 was never
jumped to. The output from `coveragetool` shows the same thing: that from line
292, only line 295 was ever jumped to. Line 302, on the other hand, is white in
the HTML report, and `coveragetool` reports that both lines 301 and 303 were
jumped to. `coveragetool` is of course miles being `Coverage` in terms of
performance and features, but given the time we had to implement it, we are
happy with it.

### Evaluation

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

## Refactoring

### Plans for refactoring

#### `utils.locate_executable`

#### `metaformat.tokenize`

#### `utils.get_structur_hash._hash`

#### `imagetools.get_image_info`
[`get_image_info` (LINK)](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/imagetools.py#L323-L401)

First, we can note that the function essentially performs two isolated tasks:

1. Parse out the filetype ([lines 324-334](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/imagetools.py#L325-L334)).
2. Parse out the width and height (rest of the function).

Now, a part of step 1 is also an early return for SVG and XML images, which are
handled separately, so these lines would be most practical to just keep in the
top-level function. Step 2 is however so self-contained that it would be easy
to put in a separate function (called maybe, `get_image_dimensions`). A large
part of the complexity of parsing the dimensions of the images stem from
parsing JPEG header data. Not only are there many branches because of the
apparent complexity of JPEG header data, but the code is also littered with
inline comments which overshadows the rest of the functionality. An obvious
refactor step would be to simply factor out
[lines 345-397](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/imagetools.py#L345-L397)
into yet another separate function (maybe called `get_jpeg_info`). This would
reduce the line count of `get_image_dimensions` considerably, and the CC as
well. `get_jpeg_info` could then be further refactored into smaller functions,
handling different corner cases of JPEG header data.

#### `cli.content_file_info_cmd`

### Performed refactoring

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
