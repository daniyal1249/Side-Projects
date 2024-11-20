
symbols = {'and': '&', 'or': '|', 'not': '~', 'implies': '>', '∧': '&', 
           '∨': '|', '¬': '~', '→': '>', '!': '~', '->': '>'}

def receive_input(symbols, prompt):
    '''
    Repeatedly asks the user for a logical expression until its in a valid format

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'
    prompt : str
        Prompt given to the user to enter a logical expression

    Returns
    -------
    expression : str
        Expression containing only allowed characters and variable names, with symbols replaced
    '''
    while True:
        invalid_chars, invalid_var = set(), False

        expression = input(prompt)
        for key, val in symbols.items():
            expression = expression.replace(key, val)

        for idx, char in enumerate(expression):
            if char not in {'(', ')', '&', '|', '~', '>', ' '} and not char.isalpha():
                invalid_chars.add(char)
            elif char.isalpha() and idx > 0 and expression[idx - 1].isalpha():
                invalid_var = True

        if invalid_chars:
            print('Character(s) not recognized:', str(invalid_chars)[1:-1])
        if invalid_var:
            print('Please use single-letter variable names.')
        
        if not (invalid_chars or invalid_var):
            break
    return expression
    

def enclosing_index(seq, idx):
    '''
    Determines the indexes of the inner-most enclosing parenthesis at a point in a sequence

    Parameters
    ----------
    seq : str or list
        Sequence to search in

    idx : int
        Nonnegative index to find the enclosing parentheses from

    Returns
    -------
    tuple
        Tuple containing the indexes of the left and right enclosing parentheses
    '''
    left_idx, right_idx = -1, len(seq)

    count = 0
    for i in range(idx - 1, -1, -1):
        if seq[i] == '(':
            count += 1
        elif seq[i] == ')':
            count -= 1
        if count == 1:
            left_idx = i
            break

    count = 0
    for i in range(idx + 1, len(seq)):
        if seq[i] == ')':
            count += 1
        elif seq[i] == '(':
            count -= 1
        if count == 1:
            right_idx = i
            break
    
    return left_idx, right_idx


def parse_expression(expression):
    '''
    Replaces all symbols in an expression with the python equivalent: 'and', 'or', or 'not'

    Parameters
    ----------
    expression : str
        Expression containing standard symbols (i.e. '&', '|', '~', or '>')

    Returns
    -------
    str
        Parsed expression with spaces between each character
    
    list
        Sorted list containing all of the variable names in the expression
    '''
    expression_lst = [char for char in expression if char != ' ']

    for idx, char in enumerate(expression_lst):
        if char == '>':
            left_idx, right_idx = enclosing_index(expression_lst, idx)
            expression_lst[right_idx:right_idx] = [')']
            expression_lst[idx:idx + 1] = [')', '|', '(']
            expression_lst[left_idx + 1:left_idx + 1] = ['~', '(']

    # Remove all instances of '()' iteratively
    expression = ''.join(expression_lst)
    while '()' in expression:
        expression = expression.replace('()', '')
    expression_lst = list(expression)
    
    symbols, vars = {'&': 'and', '|': 'or', '~': 'not'}, set()
    for idx, char in enumerate(expression_lst):
        if char in symbols:
            expression_lst[idx] = symbols[char]
        elif char.isalpha():
            vars.add(char)

    return ' '.join(expression_lst), sorted(vars)


def eval_expression(expression, vars):
    '''
    Evalutes a parsed expression for every combination of its variable's truth values

    Parameters
    ----------
    expression : str
        Parsed expression containing 'and', 'or', or 'not' as logical operators

    vars : list
        List containing all of the variable names in the expression

    Returns
    -------
    valid_vals : list or None
        - List containing the truth value combinations as dictionaries that make the expression true
        - Returns None if vars is empty
    '''
    valid_vals = []
    for i in range(2 ** len(vars)):
        values_str = f'{bin(i)[2:]:0>{len(vars)}}'
        values = [True if int(num) == 1 else False for num in values_str]
        vars_dict = {var: val for var, val in zip(vars, values)}

        try:
            if expression and eval(expression, vars_dict):  # ensure sentence is non-empty
                valid_vals.append(vars_dict)
        except SyntaxError as e:
            error_msg = str(e)
            left_idx, _ = enclosing_index(error_msg, len(error_msg) - 2)  # find ending parantheses
            print(error_msg[:left_idx])
            return None
        except Exception:
            print('invalid syntax')
            return None

    return valid_vals if vars else None


def expression_checker(symbols, prompt, display=True):
    '''
    Prompts user to enter a well-formed logical expression and evaluates it

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'
    prompt : str
        Prompt given to the user to enter a logical expression
    display : bool
        If True, function prints 'Tautology', 'Contradiction', or 'Contingency'

    Returns
    -------
    valid_vals : list or None
        - List containing the truth value combinations as dictionaries that make the expression true
        - Returns None if vars is empty
    '''
    expression = receive_input(symbols, prompt)
    expression, vars = parse_expression(expression)
    valid_vals = eval_expression(expression, vars)

    if display:
        if valid_vals is None:
            pass
        elif len(valid_vals) == 2 ** len(vars):
            print('Tautology')
        elif len(valid_vals) == 0:
            print('Contradiction')
        else:
            print('Contingency')

    return valid_vals


def main():
    expression_checker(symbols=symbols, prompt='Enter a logical expression: ')

if __name__ == '__main__':
    main()