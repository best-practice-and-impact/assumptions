# git-assumptions
Git extension for generating Markdown assumptions logs from inline comments.

Assumptions should be written inline in code using the format:

```py
# Assumption: Title of assumption
# Detailed description
# on next line or many

# Assumption: Another assumption
# Leaving an empty newline after
# the previous one
print("Code doesn't require a newline, but a non-assumption code comments do.")
```
