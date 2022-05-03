import re


def quote_check(string):
    quote_like = ['"', '|', "{" ]
    for i in quote_like:
        if i in string:
            return i
    return False


def string_reprocessing(text: str):
    '''
    The function will process the raw list of strings in ULF into a list that:
        1) correctly combines all "." with either the predicate-argument pair, as in YOU.PRO, or a simple operator node, as in .?
        2) concatenate the strings inside a quote ", bar |, or curly bracket {} into one string
    '''
    output_01 = []
    quote_like = ['"', '|', "{"]
    string = re.findall(r'[\w"]+|[(,)./!?;:=@#$%^&*_+|}{"]', text) # get the list of strings separated by all kinds of words and punctuations

    '''
    step 1, dealing with "." 
    '''
    temp = str()
    for i in string:
        if i != '.':
            if not temp:
                output_01.append(i)
            else:
                temp += i
                output_01.append(temp)
                temp = str()
        else:
            if output_01[-1] != '/':
                x = output_01.pop(-1)
                temp += x
                temp += i
            else:
                output_01.append(i)

    # step 2: dealing with quote, bar and curly brackets
    output_02 = []
    bracket = None
    temp = str()
    for i in output_01:
        if not bracket:
            if i in quote_like:
                bracket = i
                temp += i
            elif quote_check(i):
                bracket = quote_check(i)
                temp += i
            else:
                output_02.append(i)
        else:
            if i != bracket and bracket not in i:
                temp += i
            else:
                temp += i
                output_02.append(temp)
                temp = str()
                bracket = None

    return output_02


def string_read(text: str):
    string = string_reprocessing(text)
    '''
    this is the major data-reading function that reads a preprocessed string into the four desired lists. Several important features 
    in the ULF data structure were used to construct the token list and the two label lists:
        1) token name always follows a left bracket 
        2) token type always follows a slash
        3) relation type always follows a colon
    To capture the relations, we used a simple stack-in-and-out method for bracket matching. The method works well with the 
    relation type labeling, as they follow the exact same first-time-encounter order. We would be able to construct all lists we needed within one scan.
    '''
    token_list = []
    token_seq_label = []
    adjacency_label_list = []
    adjacency_list = []

    stack = []
    last = None  # 'LBS' - left bracket, 'CL' - colon, 'SL' - slash
    punkt_type_dict = {'(': 'LBS', ':': 'CL', '/': 'SL'}

    for i in string:
        if i in punkt_type_dict:
            last = punkt_type_dict[i]
            continue

        if last == 'LBS':
            token_list.append(i)
            if stack:
                top = stack[-1]
                top_index = token_list.index(top)
                adjacency_list.append((top_index, token_list.index(i)))
            stack.append(i)
        elif last == 'CL':
            adjacency_label_list.append(i)
        elif last == 'SL':
            token_seq_label.append(i)

        else:
            if i == ')':
                stack.pop(-1)

        last = None
    result = token_list, token_seq_label, adjacency_list, adjacency_label_list
    return result


'''
test_02 = '(V0 / COMPLEX :INSTANCE (V1 / K :ARG0 (V3 / REVENUE.N)) :ARG0 (V4 / COMPLEX :INSTANCE (V5 / PAST :ARG0 (V7 / RISE.V)) :ARG0 (V8 / DS :ARG0 (V10 / PERCENT) :ARG1 (V11 / "42%")) :ARG1 (V12 / ADV-A :ARG0 (V14 / TO.P :ARG0 (V16 / DS :ARG0 (V18 / CURRENCY) :ARG1 (V19 / "$133.7 million")))) :ARG2 (V20 / ADV-A :ARG0 (V22 / FROM.P :ARG0 (V24 / DS :ARG0 (V26 / CURRENCY) :ARG1 (V27 / "$94 million"))))))'
test = '(V0 / COMPLEX :INSTANCE (V1 / IF.PS :ARG0 (V3 / THEY.PRO :ARG0 (V5 / COMPLEX :INSTANCE (V6 / PRES :ARG0 (V8 / SHOULD.AUX-S)) :ARG0 (V9 / ARREST.V :ARG0 (V11 / HIM.PRO))))) :ARG0 (V12 / COMPLEX :INSTANCE (V13 / "|(|") :ARG0 (V14 / I.PRO :ARG0 (V16 / COMPLEX :INSTANCE (V17 / PRES :ARG0 (V19 / KNOW.V)) :ARG0 (V20 / THAT :ARG0 (V22 / SOMETIMES.ADV-F :ARG0 (V24 / COMPLEX :INSTANCE (V25 / K :ARG0 (V27 / PLUR :ARG0 (V29 / PRISON.N))) :ARG0 (V30 / COMPLEX :INSTANCE (V31 / PRES :ARG0 (V33 / AFFORD.V)) :ARG0 (V34 / K :ARG0 (V36 / MEANS-OF.N :ARG0 (V38 / K :ARG0 (V40 / ESCAPE.N)))))))))) :ARG1 (V41 / "|)|")) :ARG1 (V42 / COMPLEX :INSTANCE (V43 / COMPLEX :INSTANCE (V44 / PRES :ARG0 (V46 / WILL.AUX-S)) :ARG0 (V47 / YOU.PRO) :ARG1 (V48 / LEAVE.V :ARG0 (V50 / HIM.PRO) :ARG1 (V51 / IN.P :ARG0 (V53 / K :ARG0 (V55 / PRISON.N))))) :ARG0 (V56 / ?)))'
y = string_read(test_02)
'''