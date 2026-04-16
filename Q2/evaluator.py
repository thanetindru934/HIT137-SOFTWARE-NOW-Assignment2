#Assignment 2 - Q2
#Expression Evaluator using Recursive Descent Parsing.

import os

#Token types for the tokenizer.
NUM, OP, LPAREN, RPAREN, END = "NUM", "OP", "LPAREN", "RPAREN", "END"


#Tokenizer, Converts input string into tokens.
#Scans character-by-character and groups digits into multi-digit numbers
def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        # Ignore whitespace
        if ch.isspace():
            i += 1

        #Handle numbers and supports multi-digit
        elif ch.isdigit():
            num = ch
            i += 1
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append((NUM, num))

        #Handle the operators (+, -, *, /)
        elif ch in "+-*/":
            # Reject unary '+' as per requirement
            if ch == "+" and (i == 0 or expr[i-1] in "(+-*/"):
                raise Exception("Unary + not allowed")
            tokens.append((OP, ch))
            i += 1

        #handle the parentheses
        elif ch == "(":
            tokens.append((LPAREN, ch))
            i += 1
        elif ch == ")":
            tokens.append((RPAREN, ch))
            i += 1

        else:
            raise Exception("Invalid character")

    #append the END token to mark end of input
    tokens.append((END, ""))

    #handle implicit multiplication (like 2(3+4), (2+3)(4+5))
    new_tokens = []
    for i in range(len(tokens) - 1):
        t1, v1 = tokens[i]
        t2, v2 = tokens[i + 1]

        new_tokens.append(tokens[i])

        if (t1 == NUM and t2 == LPAREN) or \
           (t1 == RPAREN and t2 == NUM) or \
           (t1 == RPAREN and t2 == LPAREN):
            new_tokens.append((OP, "*"))  #insert the implicit multiplication.

    new_tokens.append(tokens[-1])
    return new_tokens


#format tokens into required output format
def format_tokens(tokens):
    return " ".join([f"[{t}:{v}]" if t != END else "[END]" for t, v in tokens])


#recursive Descent Parser (handles the operator precedence)
def parse(tokens):
    pos = 0

    def current():
        return tokens[pos]

    def eat(t=None):
        nonlocal pos
        tok = tokens[pos]
        if t and tok[0] != t:
            raise Exception("Syntax error")
        pos += 1
        return tok

    # expr --term (+/- term)
    def expr():
        node = term()
        while current()[0] == OP and current()[1] in "+-":
            op = eat(OP)[1]
            node = (op, node, term())
        return node

    # term----factor (* / factor)
    def term():
        node = factor()
        while current()[0] == OP and current()[1] in "*/":
            op = eat(OP)[1]
            node = (op, node, factor())
        return node

    # factor handles the unary negation and primary expressions.
    def factor():
        if current()[0] == OP and current()[1] == "+":
            raise Exception("Unary + not allowed")

        if current()[0] == OP and current()[1] == "-":
            eat(OP)
            return ("neg", factor())

        return primary()

    # primary---- number or parenthesized expression.
    def primary():
        tok = current()

        if tok[0] == NUM:
            eat(NUM)
            return ("num", float(tok[1]))

        elif tok[0] == LPAREN:
            eat(LPAREN)
            node = expr()
            eat(RPAREN)
            return node

        else:
            raise Exception("Syntax error")

    tree = expr()

    #ensure the  full expression is consumed
    if current()[0] != END:
        raise Exception("Extra input")

    return tree


# Convert parse tree into required prefix notation format
def tree_to_string(node):
    if isinstance(node, tuple) and node[0] == "num":
        val = node[1]
        return str(int(val)) if val.is_integer() else str(val)

    if isinstance(node, tuple) and node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if isinstance(node, tuple):
        op, left, right = node
        return f"({op} {tree_to_string(left)} {tree_to_string(right)})"

    return str(node)


#evaluate the expression tree recursively
def evaluate(node):
    if isinstance(node, tuple) and node[0] == "num":
        return node[1]

    if isinstance(node, tuple) and node[0] == "neg":
        return -evaluate(node[1])

    op, l_node, r_node = node
    l = evaluate(l_node)
    r = evaluate(r_node)

    if op == "+": return l + r
    if op == "-": return l - r
    if op == "*": return l * r
    if op == "/":
        if r == 0:
            raise Exception("Divide by zero")
        return l / r


#format the result as integer or 4 decimal places
def format_result(val):
    return str(int(val)) if val == int(val) else f"{val:.4f}"


#Main function, processes input file and writes output.txt
#Handles the tokenization, parsing, evaluation, and the error handling
def evaluate_file(input_path: str):
    results = []
    output_lines = []

    with open(input_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        expr = line.strip()

        try:
            tokens = tokenize(expr)
            tokens_str = format_tokens(tokens)

            tree = parse(tokens)
            tree_str = tree_to_string(tree)

            try:
                value = evaluate(tree)
                result_str = format_result(value)
            except Exception:
                value = None
                result_str = "ERROR"

        except Exception:
            tree_str = "ERROR"
            tokens_str = "ERROR"
            value = None
            result_str = "ERROR"

        #Stores the results as required dictionary format.
        results.append({
            "input": expr,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": result_str if result_str == "ERROR" else float(value)
        })

        # Write formatted output block
        output_lines.append(f"Input: {expr}")
        output_lines.append(f"Tree: {tree_str}")
        output_lines.append(f"Tokens: {tokens_str}")
        output_lines.append(f"Result: {result_str}")
        output_lines.append("")

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines).strip())

    return results


#Entry point, runs the program only when file is executed directly
if __name__ == "__main__":
    evaluate_file("sample_input.txt")
