
class Calculator:
    PRECEDENCE = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
    }

    def evaluate(self, expression):
        if not expression:
            return None
        tokens = expression.split()
        values = []
        operators = []

        def apply_operator():
            if len(values) < 2:
                raise ValueError("Not enough operands")
            b = values.pop()
            a = values.pop()
            op = operators.pop()
            if op == "+":
                values.append(a + b)
            elif op == "-":
                values.append(a - b)
            elif op == "*":
                values.append(a * b)
            elif op == "/":
                values.append(a / b)
            else:
                raise ValueError(f"Unsupported operator: {op}")

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit():
                values.append(int(token))
            elif token in self.PRECEDENCE:
                while (operators and
                       self.PRECEDENCE[operators[-1]] >= self.PRECEDENCE[token]):
                    apply_operator()
                operators.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")
            i += 1

        while operators:
            apply_operator()

        return values[0]
