# HIT137 – Group Assignment 2

## Repository Structure

```
├── Q1/
│   ├── program.py
│   ├── raw_text.txt
│   ├── encrypted_text.txt
│   └── decrypted_text.txt
├── Q2/
│   ├── evaluator.py
│   ├── sample_input.txt
│   └── Output.txt
└── README.md
```

---

## Question 1 – Text Encryption & Decryption

### Overview
A Python program that reads a text file, encrypts its contents using a custom shift-based cipher, decrypts the result, and verifies the decryption matches the original.

### How It Works

The encryption takes two integer inputs (`shift1`, `shift2`) and applies the following rules:

| Character | Condition | Transformation |
|---|---|---|
| Lowercase (a–m) | First half of alphabet | Shift **forward** by `shift1 × shift2` positions |
| Lowercase (n–z) | Second half of alphabet | Shift **backward** by `shift1 + shift2` positions |
| Uppercase (A–M) | First half of alphabet | Shift **backward** by `shift1` positions |
| Uppercase (N–Z) | Second half of alphabet | Shift **forward** by `shift2²` positions |
| Other characters | Spaces, numbers, symbols | Unchanged |

### Files

| File | Description |
|---|---|
| `program.py` | Main program – encryption, decryption, and verification logic |
| `raw_text.txt` | Original input text |
| `encrypted_text.txt` | Output of the encryption function |
| `decrypted_text.txt` | Output of the decryption function |

### Usage

```bash
cd Q1
python program.py
```

When run, the program will:
1. Prompt you to enter `shift1` and `shift2` values
2. Encrypt `raw_text.txt` → `encrypted_text.txt`
3. Decrypt `encrypted_text.txt` → `decrypted_text.txt`
4. Verify that `decrypted_text.txt` matches `raw_text.txt` and print the result

---
The encryption function writes a marker after each transformed letter to record which rule was applied. During decryption, these markers are read to reverse the exact shift and recover the original text.

## Question 2 – Mathematical Expression Evaluator

### Overview
A Python program that reads mathematical expressions from a text file (one per line), parses and evaluates each using **recursive descent parsing**, and writes the results to an output file.

The solution is built entirely from plain functions (no classes). Operator precedence is handled by separate functions: `expr()` for `+ -`, `term()` for `* /`, `factor()` for unary negation, and `primary()` for numbers or parentheses.

### Supported Features
- Basic operators: `+`, `-`, `*`, `/`
- Parentheses nested to any depth
- Unary negation (e.g. `-5`, `--5`, `-(3+4)`)
- Implicit multiplication (e.g. `2(3+4)` or `(2+3)(4+5)`)
- Unary `+` is **not** supported and produces `ERROR`

### Output Format
For each expression, the output file contains a four-line block:
```
Input: <original expression>
Tree: <parse tree representation>
Tokens: <token list>
Result: <computed value or ERROR>
```

**Example:**
```
Input: 3 + 5
Tree: (+ 3 5)
Tokens: [NUM:3] [OP:+] [NUM:5] [END]
Result: 8
```

Blocks are separated by a blank line. Results that are whole numbers are displayed without a decimal point; otherwise they are rounded to 4 decimal places.

### Token Types

| Token | Meaning |
|---|---|
| `NUM` | A numeric literal |
| `OP` | An operator (`+`, `-`, `*`, `/`) |
| `LPAREN` | Opening parenthesis `(` |
| `RPAREN` | Closing parenthesis `)` |
| `END` | End of input |

### Files

| File | Description |
|---|---|
| `evaluator.py` | Main evaluator – tokeniser, parser, and evaluator logic |
| `sample_input.txt` | Sample expressions used for testing |
| `Output.txt` | Corresponding output produced by the program |

### Usage

```bash
cd Q2
python evaluator.py
```

Or use the module interface directly in Python:

```python
from evaluator import evaluate_file

results = evaluate_file("sample_input.txt")
```

`evaluate_file(input_path)` returns a list of dictionaries, one per expression:

```python
[
    {"input": "3 + 5", "tree": "(+ 3 5)", "tokens": "[NUM:3] [OP:+] [NUM:5] [END]", "result": 8.0},
    {"input": "3 @ 5", "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"},
]
```

The output file `output.txt` is written to the same directory as the input file.

---

## Requirements

- Python 3.x
- No external libraries required

---

## Submission

- GitHub repository link is included in `github_link.txt`
