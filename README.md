# [gen]erate LLM completions

A basic CLI wrapper of LLM providers with an interface to review suggested file
diffs before applying them. Read the [manifesto](MANIFESTO.md) for an idea of
where a potential roadmap would lead. I have no formal plans.

See basic usage below or look at a few [examples.](examples/)


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
$ gen -e "use placeholders instead of f strings" program1.py
---
+++
@@ -1,7 +1,8 @@
 def user_confirmation(question):
-    answer = input(f'{question} [y/N]: ')
+    answer = input('{} [y/N]: '.format(question))

     while answer.lower() not in {'y', 'n'}:
         return user_confirmation(question)

     return answer == 'y'

Confirm changes to program1.py [y/N]:
```

Provide as many files as you need for added context.


```
$ gen -e "any edge cases i havent thought to test?" test_program1.py -c program1.py program1_dep.py

[... and maybe you get a useful response]
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
