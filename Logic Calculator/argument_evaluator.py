import expression_evaluator as ee

def receive_expression(symbols, prompt):
    '''
    '''
    while True:
        expression = input(prompt)
        for key, val in symbols.items():
            expression = expression.replace(key, val)

        if expression[:2] == 'P:':
            premise = True
            break
        elif expression[:2] == 'C:':
            premise = False
            break
        else:
            print('Please begin your expression with \'P:\' for premise or \'C:\' for conclusion.')
    return expression[2:], premise


def receive_argument(symbols):
    '''
    //

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'

    Returns
    -------
    str
        The combined argument in the form: premise1 & premise2 & ... > conclusion
    '''
    premises = []
    line = 1
    while True:
        expression, premise = receive_expression(symbols=symbols, prompt=f'Line {line}: ')
        if not premise:
            break
        premises.append(f'({expression})')
        line += 1

    return '&'.join(premises) + f'>({expression})'


def argument_checker(symbols):
    '''
    //

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'

    Returns
    -------
    None
    '''
    argument = receive_argument(symbols)
    invalid_chars, invalid_var = set(), False

    for idx, char in enumerate(argument):
        if char not in {'(', ')', '&', '|', '~', '>', ' '} and not char.isalpha():
            invalid_chars.add(char)
        elif char.isalpha() and idx > 0 and argument[idx - 1].isalpha():
            invalid_var = True

    if invalid_chars:
        print('Character(s) not recognized:', str(invalid_chars)[1:-1])
    if invalid_var:
        print('Please use single-letter variable names.')
    if invalid_chars or invalid_var:
        return None
    
    argument, vars = ee.parse_expression(argument)
    valid_vals = ee.eval_expression(argument, vars)

    if valid_vals is None:
        pass
    elif len(valid_vals) == 2 ** len(vars):
        print('Valid')
    else:
        print('Invalid')


def main():
    argument_checker(symbols=ee.symbols)

if __name__ == '__main__':
    main()