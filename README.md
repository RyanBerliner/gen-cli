# [gen]erate LLM completions

A basic CLI tool to generate LLM completions. Read from stdin or files, write
to stdout or back to files.

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

Edit a file, or multiple files sequentially.

```
$ gen -e "convert from % to f-strings" program1.py program2.py
program1.py
program2.py
```

## Installation

1. **Clone this repo and alias ./cli.py to whatever command you wish to use.**
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
model = llama3.1:8b-instruct-q6_K

[fast]
provider = ollama
endpoint = http://<ollama-endpoint>
model = llama3.2:1b
```

### Supported Provider Configurations

| Provider | Model    | Endpoint     | Key      | Effort   |
|:---------|:---------|:-------------|:---------|:---------|
| cerebras | required | n/a          | required | required |
| grok     | required | n/a          | required | required |
| ollama   | required | required[^1] | n/a      | n/a      |

[^1]: Do not include the path. An example valid endpoint is http://localhost:8000
