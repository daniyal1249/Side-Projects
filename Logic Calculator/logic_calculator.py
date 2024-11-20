
symbols = {'and': '&', 'or': '|', 'not': '~', 'implies': '>', '∧': '&', 
           '∨': '|', '¬': '~', '→': '>', '!': '~', '->': '>'}

def receive_input(symbols):
    '''
    Repeatedly asks the user for a logical expression until its in a valid format

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'

    Returns
    -------
    sentence : str
        Expression containing only allowed characters and variable names, with symbols replaced
    '''
    while True:
        invalid_chars, invalid_var = set(), False

        sentence = input('Enter a logical expression: ')
        for key, val in symbols.items():
            sentence = sentence.replace(key, val)

        for idx, char in enumerate(sentence):
            if char not in {'(', ')', '&', '|', '~', '>', ' '} and not char.isalpha():
                invalid_chars.add(char)
            elif char.isalpha() and idx > 0 and sentence[idx - 1].isalpha():
                invalid_var = True

        if invalid_chars:
            print('Character(s) not recognized:', str(invalid_chars)[1:-1])
        if invalid_var:
            print('Please use single-letter variable names.')
        
        if not (invalid_chars or invalid_var):
            break
    return sentence
    

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


def parse_sentence(sentence):
    '''
    Replaces all symbols in a sentence with the python equivalent: 'and', 'or', or 'not'

    Parameters
    ----------
    sentence : str
        Sentence containing standard symbols (i.e. '&', '|', '~', or '>')

    Returns
    -------
    str
        Parsed sentence with spaces between each character
    
    list
        Sorted list containing all of the variable names in the sentence
    '''
    sentence_lst = [char for char in sentence if char != ' ']

    for idx, char in enumerate(sentence_lst):
        if char == '>':
            left_idx, right_idx = enclosing_index(sentence_lst, idx)
            sentence_lst[right_idx:right_idx] = [')']
            sentence_lst[idx:idx + 1] = [')', '|', '(']
            sentence_lst[left_idx + 1:left_idx + 1] = ['~', '(']

    # Remove all instances of '()' iteratively
    sentence = ''.join(sentence_lst)
    while '()' in sentence:
        sentence = sentence.replace('()', '')
    sentence_lst = list(sentence)
    
    symbols, vars = {'&': 'and', '|': 'or', '~': 'not'}, set()
    for idx, char in enumerate(sentence_lst):
        if char in symbols:
            sentence_lst[idx] = symbols[char]
        elif char.isalpha():
            vars.add(char)

    return ' '.join(sentence_lst), sorted(vars)


def eval_sentence(sentence, vars):
    '''
    Evalutes a parsed sentence for every combination of its variable's truth values

    Parameters
    ----------
    sentence : str
        Parsed sentence containing 'and', 'or', or 'not' as logical operators

    vars : list
        List containing all of the variable names in the sentence

    Returns
    -------
    valid_vals : list or None
        - List containing the truth value combinations as dictionaries that make the sentence true
        - Returns None if vars is empty
    '''
    valid_vals = []
    for i in range(2 ** len(vars)):
        values_str = f'{bin(i)[2:]:0>{len(vars)}}'
        values = [True if int(num) == 1 else False for num in values_str]
        vars_dict = {var: val for var, val in zip(vars, values)}

        try:
            if sentence and eval(sentence, vars_dict):  # ensure sentence is non-empty
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


def logic_checker(symbols, display=True):
    '''
    Prompts user to enter a well-formed logical expression and evaluates it

    Parameters
    ----------
    symbols : dict
        Dictionary containing the allowed symbols/keywords paired with '&', '|', '~', or '>'
    display : bool
        If True, function prints 'Tautology', 'Contradiction', or 'Contingency'

    Returns
    -------
    valid_vals : list or None
        - List containing the truth value combinations as dictionaries that make the sentence true
        - Returns None if vars is empty
    '''
    sentence = receive_input(symbols)
    sentence, vars = parse_sentence(sentence)
    valid_vals = eval_sentence(sentence, vars)

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
    logic_checker(symbols)

if __name__ == '__main__':
    main()