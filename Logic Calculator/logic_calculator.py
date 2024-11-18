
symbols = {'and': '&', 'or': '|', 'not': '~', 'implies': '>', '∧': '&', 
           '∨': '|', '¬': '~', '→': '>', '!': '~'}

def receive_input(symbols):
    while True:
        invalid_chars, invalid_var = set(), False

        sentence = input('Enter a logical expression (or type \'E\' to exit): ')
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
    sentence_lst = [char for char in sentence if char != ' ']

    for idx, char in enumerate(sentence_lst):
        if char == '>':
            left_idx, right_idx = enclosing_index(sentence_lst, idx)
            sentence_lst[right_idx:right_idx] = [')']
            sentence_lst[idx:idx + 1] = [')', '|', '(']
            sentence_lst[left_idx + 1:left_idx + 1] = ['~', '(']
    print(''.join(sentence_lst))  # for debugging

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
    valid_vals = []
    for i in range(2 ** len(vars)):
        values_str = f'{bin(i)[2:]:0>{len(vars)}}'
        values = [True if int(num) == 1 else False for num in values_str]
        vars_dict = {var: val for var, val in zip(vars, values)}

        try:
            if eval(sentence, vars_dict):
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


def main():
    while True:
        sentence = receive_input(symbols)
        sentence, vars = parse_sentence(sentence)
        valid_vals = eval_sentence(sentence, vars)

        if sentence.upper() == 'E':
            break

        if valid_vals is None:
            pass
        elif len(valid_vals) == 2 ** len(vars):
            print('Tautology')
        elif len(valid_vals) == 0:
            print('Contradiction')
        else:
            print('Contingency')

if __name__ == '__main__':
    main()