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

Neither of us got the same results as `lizard`, and because we used slightly
different methods for computing the CC we also got different results for most
of the five functions we measured manually. One of us used the method presented
in class and the other one of us used [this
method](https://www.aivosto.com/project/help/pm-complexity.html). The
difference is that the latter does not take the number of exits and boolean
operators into account. Our results were as follows:

| Method                                             | CC lecture | CC alternative |
|----------------------------------------------------|------------|----------------|
| `find_files@sourcesearch.py`                       | 5          | 4              |
| `coerce@db.py`                                     | 9          | 10             |
| `merge@utils.py`                                   | 7          | 7              |
| `content_file_info_cmd@cli.py`                     | 11         | 11             |
| `discover_relevant_flowblock_models@types/flow.py` | 8          | 9              |
| `get_image_info@imagetools.py`                     | 10         | 13             |

The functions we chose are of varying complexity. We also included the
`find_files` method to show that even though it is almost 40 lines of code,
which is longer than most of the other functions we measured, it still has a
relatively low CC. This goes to show that high CC does not necessarily imply
a long and complicated function.

Lizard seems to count every try, except and finally as one decision each. In
our interpretation of the lecture slides, every `try` statement counts as one
decision no matter how many `except`’s and `finally`’s it has. In our other method,
every `except` counts as one decision.

The documentation is very lacking in all the functions we chose. Some of them
have no documentation at all while others have a few lines explaining the
general idea of the function, but never anything about all possible outcomes.
None of them use proper docstrings. We also noted that the functions we chose
from `lektor/cli.py` are mistakenly stated to return values, which is wrong
since they only write to stdout/stderr.

### Condensation graphs
We created condensation graphs for some of the functions we chose to analyze. Here is the condensation graph we created for the function `utils.merge`

![utils.merge](graphs/merge.png)

A square node represents one or more statements and a diamond node represent a condition. Green arrows is the path chosen if the condition evaluates to true and red arrows is the path chosen if the condition evaluates to false. The number in each node represents the line number of which the statement/condition occurs in the original code.

see [graphs](graphs/) for all condensation graphs.

### Function purposes

* `utils.merge`:
Merge two lists/dictionary values together.

* `metaformat.tokenize`:
Tokenizes an iterable of newlines as bytes into key value pairs out of the lektor bulk format.  By default it will process all fields, but optionally it can skip values of uninteresting keys and will instead yield `None`. This will not perform any other processing on the data other than decoding and basic tokenizing.

* `lektor.utils.decode_flat_data`:
Decodes data from an iterator given from parsing a .ini file into a dictionary of the given dictionary type, or a regular dictionary if no argument is given.

* `lektor.utils.prune_file_and_folder`:
Takes a “name” filepath and a “base” filepath, where the latter is supposed to be a parent directory of the former. The method then repeatedly tries deleting the file or folder at the “name” filepath while walking higher up in the hierarchy until it fails, either because it reaches the “base” filepath or a non-empty subdirectory of the “base” filepath.

* `lektor.cli.content_file_info_cmd`
CLI command for printing out information about Lektor project files.

* `lektor.imagetools.get_image_info`
Utility command for parsing header info in `png`, `jpg`, `svg` and `gif` images. More specifically, given a file descriptor, it returns filetype, height and width if the image is supported. For unsupported file formats, it just returns `(None, None, None`).

* `lektor.utils.get_structure_hash`:
Given a Python structure, this generates a md5 hash. The method maps python structures to bytes which the md5 gets updated with and later digested. Not all Python types are supported, but quite a few are.

* `lektor.utils.locate_executable`:
Searches and returns the first found path to an executable file. Takes the name of the executable file to search for and current working directory.

* `lektor.db.coerce`:
Takes two parameters _a_ and _b_ and coerces them to be comparable. Comparable
in this case means having the same type or one of them being `None`. For example
if a is an `int` and b is a `float`, this method makes b an `int`.

* `lektor.types.flow.discover_relevant_flowblock_models`:
First some terminology. A flow is just a bunch of flowblocks. It's not important to know exactly what a flowblock is, but they are basically a set of properties with a unifying name. The function will try to find and return every flowblock given a list of flowblock names and a target database. Or, if no names are provided, it will instead return all the flowblocks from the target database.

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
[`utils.locate_executable`](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/utils.py#L274-L309)

If the name of the executable file given as a parameter is not a path the
function will enter a [section](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/utils.py#L291-L297)
that resolves this by appending paths from the os environment variable $PATH as
choices of places to look for executables. That section could be split into a
seperate function and doing so will decrease the overall CC of
`locate_executable`. Also, the [last part](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/utils.py#L302-L309)
of the function does the actual searching and before that it just listed the
valid paths and extensions to use in the searching. That last part could be
split into a seperate function that takes the paths and extensions to look for
and then return whatever that function returns.

#### `metaformat.tokenize`
[`metaformat.tokenize` (LINK)](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/metaformat.py#L18-L76)

Almost all the complexity of this function lies in the
[for-loop](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/metaformat.py#L46-L73).
However, since it relies heavily on the local variables declared at the top of
the function, refactoring this part would result in a function with a lot of
arguments. Due to this, our conclusion is that this would not improve the code
in terms of readability and that it would take a lot of work to make a clean
refactoring.

#### `utils.get_structure_hash._hash`
[`utils.get_structure_hash`](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/utils.py#L554-L582)  

This function is basically a switch statement checking what type of object the
parameter is and updating the hash accordingly. Different types of objects
updates the hash differently. Each case has a very simple body, making a
refactoring here not worth it. There is no part of the code that is reusable.
Changing a statement would alter the functionality. Generally speaking, switch
statements, or similar, are not viable for refactoring.

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
[`content_file_info_cmd` (LINK)](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/cli.py#L426-L479)

This function is a CLI command to print information about Lektor project files.
We can note that it performs several distinct tasks:

1. Define a `fail` function that prints an error message and then causes a
   system exit ([lines 439-443](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/cli.py#L439-L443)).
2. Extract the related Lektor project.
   ([lines 445-452](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/cli.py#L445-L455)).
    - This includes verifying that all files are related to the the same project.
3. Extract actual content files ([lines 457-464](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/cli.py#L457-L464))
4. Print non-error results ([lines 466-472](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/cli.py#L466-L479))

This is almost trivial to split into smaller parts: simply extract each of the
steps into different functions. Steps 2-3 require the `fail` function defined
in step 1, which could be provided either as a callback, or simply defining
`fail` as a standalone function. The remaining dependencies between steps
are easily resolved. Step 3 requires the project from step 2, and step 4
requires both the project from step 2 and the content files from step 3, but
that's pretty much it.

#### `db.coerce`
[`db.coerce` (LINK)](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/db.py#L110-L131)

This function is used to convert the variables to a form which allows them to
be compared. All the outer if-statements contain code for handling specific
combinations of types. The first two seem a bit small to split into separate
functions, since they almost contain no logic. [The third
if-statement](https://github.com/slarse/lektor/blob/3d82277a04d2e40fdc8b7dce451c9201c5362c9c/lektor/db.py#L115-L120)
can be split into a separate method and the last two could be placed in a
separate function. To further decrease the CC, one could replace the last `or`
statements with a function call.

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
