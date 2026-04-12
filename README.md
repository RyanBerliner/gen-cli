# [gen]erate LLM completions

A basic CLI wrapper of LLM providers with an interface to review suggested file
diffs before applying them. Read the [manifesto](MANIFESTO.md) for an idea of
where a potential roadmap would lead. I have no formal plans.


## Basic Usage

Run `gen -h` for all options. Generations below are purely illustrative.

Generate a response to a prompt.

```
$ gen "show me an example of python dict comprehension"
{key: value for key, value in {'a': 1, 'b': 2}.items()} 
```

Add context from stdin

```
$ git log -n 3 | gen "categorize each commit as chore, feature, bugfix"
bugfix: fix race condition in data pipeline
chore: remove unused variable
chore: update runtime dependencies
```

Ask about a file, or multiple files sequentially.

```
$ gen "what's this commenting style called" program.py
Docstring
```

Edit a file. Review the diff before confirming, or use `--force` to write
without review.

```
$ gen -e "extract the ansi codes into named constants so this reads better" program1.py
---
+++
@@ -7,6 +7,12 @@
     GREEN = "\x1b[32m"
     RED = "\x1b[31m"
     RESET = "\x1b[0m"
+    ENTER_ALT_SCREEN = '\x1b[?1049h'
+    HIDE_CURSOR = '\x1b[?25l'
+    CLEAR_TO_END = '\x1b[?1049h'
+    MOVE_CURSOR_TOP_LEFT = '\x1b[0;0H'
+    SHOW_CURSOR = '\x1b[?25h'
+    LEAVE_ALT_SCREEN = '\x1b[?1049l'

     def __init__(self, file):
         self.start_contents = file.readlines()
@@ -55,17 +61,17 @@
         # scrollback history, especially in tmux

         # enter alt screen
-        sys.stdout.write('\x1b[?1049h')
+        sys.stdout.write(self.ENTER_ALT_SCREEN)
         # hide cursor
-        sys.stdout.write('\x1b[?25l')
+        sys.stdout.write(self.HIDE_CURSOR)
         # clear to the end
-        sys.stdout.write('\x1b[?1049h')
+        sys.stdout.write(self.CLEAR_TO_END)
         # move to top left
-        sys.stdout.write('\x1b[0;0H')
+        sys.stdout.write(self.MOVE_CURSOR_TOP_LEFT)

         self.show_output(final=False)

         # show cursor
-        sys.stdout.write('\x1b[?25h')
+        sys.stdout.write(self.SHOW_CURSOR)
         # leave alt screen
-        sys.stdout.write('\x1b[?1049l')
+        sys.stdout.write(self.LEAVE_ALT_SCREEN)

Confirm changes to program1.py [y/N]:
```

## Installation

1. **Clone this repo and alias `cli.py` to whatever command you wish to use.**
   `gen` is recommended and used in the examples in this readme. You will need
   Python to be installed, that is the only dependency.

2. **Set up the required prompts.** These must live in `~/.gen` and you can
   easily use the defaults by symlinking those found in this repo under
   `.gen/`. You can rewrite these as you see need, or just keep using the
   defaults.

3. **Add your LLM provider(s)**. To generate the completions you'll need to
   point the tool to a supported provider via `~/.gen/config` profiles. Read
   more in the Configuration section below.


## Configuration

You configure and use multiple profiles with `--profile`. These are stored in
`~/.gen/config` with the following options. You **must** define a default
profile.

```
[default]
provider = ollama
endpoint = http://<ollama-endpoint>
model = gemma4:e2b

[fast]
provider = ollama
endpoint = http://<ollama-endpoint>
model = llama3.2:1b
```

### Supported Provider Configurations

| Provider | Model    | Endpoint     | Key      | Effort   |
|:---------|:---------|:-------------|:---------|:---------|
| cerebras | required | n/a          | required | optional |
| grok     | required | n/a          | required | optional |
| ollama   | required | required[^1] | n/a      | n/a      |
| openai   | required | n/a          | required | optional |

[^1]: Do not include the path. An example valid endpoint is http://localhost:8000
