#!/bin/bash

# This example script performs a code review on a commit range, such as
#
# Last 5 commits
# code-review.sh HEAD~5..HEAD
#
# Changes on a branch (ie from master)
# code-review.sh master..HEAD
#
# .. any commit range will suffice.

REVIEW_INSTRUCTIONS=$(cat <<'EOF'

Review the code changes. I've provided the diffs with commit messages, and also
the full files as additional context. I would like you to review the code for

- Accuracy, does it do what it should, are there logic bugs
- Unhandled edge cases, is something missing
- Beating around the bush, is there a simpler way to implement something
- Typos, either in variable names, comments, or prose

If there is nothing to note, say that it looks good... you do not NEED to
provide feedback if you don't see anything worth noting. I don't want nitpicks.
Also please don't suggest changes on code that wasn't changed in the diff.

If you do have feedback to give, please output your feedback by first quoting
code that you are referring to inside a \`\`\` block, and then providing your
feedback on that code block directly after. If you have a suggested fix, you
can include an explanation of what you'd like to see with short code snippets
or short pseudo code... but don't babble on or provide giant pieces of code.

EOF
)

gen "$REVIEW_INSTRUCTIONS\n\n$(git show "$1")" -c $(git diff --name-only "$1")
