#Assignment 2 - Q2
#Expression Evaluator (Recursive Descent)

import os

#Token types
NUM, OP, LPAREN, RPAREN, END = "NUM", "OP", "LPAREN", "RPAREN", "END"



#Tokenizer

def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        #Ignore spaces
        if ch.isspace():
            i += 1

        #Numbers (multi-digit)
        elif ch.isdigit():
            num = ch
            i += 1
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append((NUM, num))

        #Operators
        elif ch in "+-*/":
            #Reject unary +
            if ch == "+" and (i == 0 or expr[i-1] in "(+-*/"):
                raise Exception("Unary + not allowed")
            tokens.append((OP, ch))
            i += 1

        #Parentheses
        elif ch == "(":
            tokens.append((LPAREN, ch))
            i += 1

        elif ch == ")":
            tokens.append((RPAREN, ch))
            i += 1

        else:
            raise Exception("Invalid character")

    #Add END token
    tokens.append((END, ""))

  
    #Implicit multiplication handling
    
    new_tokens = []
    for i in range(len(tokens)-1):
        new_tokens.append(tokens[i])

        #NUM followed by LPAREN → insert *
        if tokens[i][0] == NUM and tokens[i+1][0] == LPAREN:
            new_tokens.append((OP, "*"))

        #RPAREN followed by NUM → insert *
        if tokens[i][0] == RPAREN and tokens[i+1][0] == NUM:
            new_tokens.append((OP, "*"))

    new_tokens.append(tokens[-1])

    return new_tokens


#Format tokens into required string format
def format_tokens(tokens):
    return " ".join([f"[{t}:{v}]" if t != END else "[END]" for t, v in tokens])



#Parser (Recursive Descent)

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

    #Expression → handles + and -
    def expr():
        node = term()
        while current()[0] == OP and current()[1] in "+-":
            op = eat(OP)[1]
            node = (op, node, term())
        return node

    #Term -- handles * and /
    def term():
        node = factor()
        while current()[0] == OP and current()[1] in "*/":
            op = eat(OP)[1]
            node = (op, node, factor())
        return node

    # Factor -- handles unary negation
    def factor():
        if current()[0] == OP and current()[1] == "-":
            eat(OP)
            return ("neg", factor())
        return primary()

    #Primary, numbers or parentheses
    def primary():
        tok = current()

        if tok[0] == NUM:
            eat(NUM)
            return int(tok[1])

        elif tok[0] == LPAREN:
            eat(LPAREN)
            node = expr()
            eat(RPAREN)
            return node

        else:
            raise Exception("Syntax error")

    tree = expr()

    #Ensure no extra input remains
    if current()[0] != END:
        raise Exception("Extra input")

    return tree



#Convert tree to string format

def tree_to_string(node):
    if isinstance(node, int):
        return str(node)

    if node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    op, left, right = node
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"



#Evaluate expression tree

def evaluate(node):
    if isinstance(node, int):
        return float(node)

    if node[0] == "neg":
        return -evaluate(node[1])

    op, l, r = node[0], evaluate(node[1]), evaluate(node[2])

    if op == "+": return l + r
    if op == "-": return l - r
    if op == "*": return l * r
    if op == "/":
        if r == 0:
            raise Exception("Divide by zero")
        return l / r


#Format result as required
def format_result(val):
    if val == int(val):
        return str(int(val))
    return f"{val:.4f}"



#Main function (Required Interface)

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
                result_str = "ERROR"

        except Exception:
            tree_str = "ERROR"
            tokens_str = "ERROR"
            result_str = "ERROR"

        results.append({
            "input": expr,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": result_str if result_str == "ERROR" else float(value)
        })

        output_lines.append(f"Input: {expr}")
        output_lines.append(f"Tree: {tree_str}")
        output_lines.append(f"Tokens: {tokens_str}")
        output_lines.append(f"Result: {result_str}")
        output_lines.append("")

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines).strip())

    return results


#Run directly
if __name__ == "__main__":
    evaluate_file("sample_input.txt")