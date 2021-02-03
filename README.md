# Assumptions

Generating Markdown assumptions logs from code comments. This command line tool is build in Python, but can be used to collect assumptions from any files that support hash (`#`) comments.

## Usage

Run the command line tool to generate help documentation:

```sh
python assumptions.py -h
```

## Assumptions

Assumptions can be written in code files using the following format:

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
# "Q" and "I" can be used for shorthand RAG-rating categories.
print("Code doesn't require a newline")

    # Assumption: Yet another assumption
    # Q: RED
    # I: GREEN
    # Indented? No problem.

    # But non-assumption comments do require an empty newline.
```

Quality and Impact RAG-ratings are used, according to the following definitions. These have been defined by the Home Office Analytical Quality Assurance team:

| RAG   | Assumption quality                                                                                                              | Assumption impact                                                                           |
|-------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| GREEN | Reliable assumption, well understood and/or documented; anything up to a validated & recent set of actual data.                 | Marginal assumptions; their changes have no or limited impact on the outputs.               |
| AMBER | Some evidence to support the assumption; may vary from a source with poor methodology to a good source that is a few years old. | Assumptions with a relevant, even if not critical, impact on the outputs.                   |
| RED   | Little evidence to support the assumption; may vary from an opinion to a limited data source with poor methodology.             | Core assumptions of the analysis; the output would be drastically affected by their change. |

## Outputs

The collected assumptions are represented in the output log as:

```md
### Assumption 1: Title of assumption

* Location: `search_here/good.py`
* **Quality**: RED
* **Impact**: AMBER

Detailed description on next line or many.

### Assumption 2: Another assumption

* Location: `search_here/good.py`
* **Quality**: GREEN
* **Impact**: RED

Leaving an empty newline after the previous one. Q and I can be used for shorthand RAG ratings.

### Assumption 3: Yet another assumption

* Location: `search_here/good.py`
* **Quality**: RED
* **Impact**: GREEN

Indented? No problem.
```
