# git-assumptions
Git extension for generating an assumptions log from inline comments.

Assumptions should be written inline in code using the format:

```
# Assumption: Title of assumption
# Detailed description
# on next line or many

# Assumption: Another assumption
# Leaving an empty newline after
# the previous one
print("But code doesn't require a newline")
```
