# Token Count CLI

`token_count_cli.py` is a Python command-line tool that calculates the token count in files within a directory, displaying a tree structure of folders and files within the specified directory, sorted by their token count. Its primary purpose is to quickly assess if a directory or repository's contents can be loaded into GPT-4 (which has a token limit of 8,000 tokens) by analyzing the cumulative token count. Furthermore, it helps identify any unnecessary files that might skew the token distribution, allowing you to make better decisions on excluding those files before loading the content into GPT-4.

## Features

- Tokenizes files using `tiktoken` with customizable encoding
- Skips files with UnicodeDecodeError
- Ignores `.git` and `venv` directories by default
- Calculates and displays total token count within folders
- Displays tree structure with folder icons and token counts
- Folders and files sorted by token count by default

## Dependencies

- [tiktoken](https://github.com/openai/tiktoken)

## Usage

1. Ensure you have Python 3.6+ and `tiktoken` library installed.

2. Download and save `token_count_cli.py` to your local machine.

3. Run the following command in your terminal:

```bash
python token_count_cli.py DIRECTORY [--encoding ENCODING]
```

- `DIRECTORY`: Path to the target directory containing the files
- `--encoding`: (Optional) The name of the encoding method used by tiktoken (default: `cl100k_base`)

The tool will output the tree structure of the directory with the token counts displayed next to each file and folder.

## Example

Given a project directory like this:

```
project/
│
├── main.py
├── utils/
│   ├── util_a.py
│   └── util_b.py
└── data/
    ├── data_a.csv
    └── data_b.csv
```

Running `token_count_cli.py` on the `project` directory will output something similar to:

```
Number of skipped files: 0

📂 project (500 tokens)
│   ├── 📂 utils (300 tokens)
│   │   ├── util_b.py: 200 tokens
│   │   └── util_a.py: 100 tokens
│   ├── 📂 data (0 tokens)
│   └── main.py: 200 tokens
```

In this example, the total token count is 500, and you can easily see if there are any unnecessary files adding to the token count.
