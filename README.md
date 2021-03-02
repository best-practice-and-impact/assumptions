# Assumptions

Acknowledging the assumptions and caveats in our analysis is an essential part of quality assurance.
When the code changes, this should be reflected in our documentation.

Record your analytical assumptions and caveats in code comments:

```py
# Assumption: Title of assumption
# Quality: RED
# Impact: AMBER
# Detailed description
# on one line or many.
```

Assumptions will generate a Markdown assumptions logs for your documentation:

```markdown
### Assumption 1: Title of assumption

* Location: `test_git_assumptions/search_here/assumptions.py`
* **Quality**: RED
* **Impact**: AMBER

Detailed description on one line or many.
```

## Installation and Usage

The Python package can currently be installed from GitHub:

```sh
pip install git+https://github.com/foster999/assumptions.git
```

Run the command line tool to generate help documentation:

```sh
assumptions -h
```

By default, the tool will recursively search the current directory for assumptions and caveats, before writing the log to the same directory.

## Assumptions and caveats log

### Assumptions

Assumptions can be written in code files using the following formats:

```py
# Assumption: Title of assumption
# Quality: RED
# Impact: AMBER
# Detailed description
# on next line or many.

# Assumption: Another assumption
# Q: GREEN
# I: RED
# Leaving an empty newline after
# the previous one.
#
# Q and I can be used for shorthand RAG ratings.
print("Code doesn't require a newline")

for something in things:
    # Assumption: Yet another assumption
    # Q: RED
    # I: GREEN
    # Indented? No problem.

    # But non-assumption comments do require an empty newline.
    do(something)
```
Assumptions are rated red, amber or green (RAG) to record the quality and risk associated with each assumption:

| RAG rating | Assumption quality | Assumption impact |
|------------|--------------------|-------------------|
| GREEN | Reliable assumption, well understood and/or documented; anything up to a validated & recent set of actual data. | Marginal assumptions; their changes have no or limited impact on the outputs.  |
| AMBER | Some evidence to support the assumption; may vary from a source with poor methodology to a good source that is a few years old. | Assumptions with a relevant, even if not critical, impact on the outputs. |
| RED   | Little evidence to support the assumption; may vary from an opinion to a limited data source with poor methodology. | Core assumptions of the analysis; the output would be drastically affected by their change. |

### Caveats

Caveats are simpler, with only a title and detailed description:

```py
# Caveat: Oh oh
# Something isn't quite what it seems
```

### Output log

The collected assumptions and caveats are represented in an output log as:

```md
### Assumption 1: Title of assumption

* Location: `test_git_assumptions/search_here/assumptions.py`
* **Quality**: RED
* **Impact**: AMBER

Detailed description on next line or many.

### Assumption 2: Another assumption

* Location: `test_git_assumptions/search_here/assumptions.py`
* **Quality**: GREEN
* **Impact**: RED

Leaving an empty newline after the previous one. Q and I can be used for shorthand RAG ratings.

### Assumption 3: Yet another assumption

* Location: `test_git_assumptions/search_here/assumptions.py`
* **Quality**: RED
* **Impact**: GREEN

Indented? No problem.

### Caveat 1: Oh oh

Location: `test_git_assumptions/search_here/caveats.py`

Something isn't quite what it seems
```

## Extensibility

Custom templates can be passed to the command line interface (CLI) to use alternative text in the log output.

The tool can be easily extended to capture other patterns from text files, by created custom `LogItem` subclasses. See the existing classes to understand how these should be structure. See the CLI to understand how these can be used with the main `Log` class.

Please consider creating a Pull Request to incorporate new templates and log items into the CLI tool.
