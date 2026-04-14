#!/bin/bash

# This exaple script performs a code review on a commit range, such as
#
# Last 5 commits
# code-review.sh HEAD~5..HEAD
#
# Changes on from a branch (ie master)
# code-review.sh master..HEAD

REVIEW_INSTRUCTIONS=$(cat <<'EOF'

Review the code changes. I've provided the diffs with commit messages, and also
the full files as additional context. I would like you to review the code for

- Accuracy, does it do what it should, are there logic bugs
- Unhandled edge cases, is something missing
- Beating around the bush, is there a simpler way to implement something
- Typos, either in variable names, comments, or prose

If there is nothing to note, say that it looks good... you do not NEED to
provide feedback if you dont see anything worth noting. I don't want nit picks.
Also please don't suggest changes on code that wasn't changed in the diff.

EOF
)

gen "$REVIEW_INSTRUCTIONS\n\n$(git show $1)" -c $(git diff --name-only $1)
