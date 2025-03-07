def isValid(s):
    pair_paranthesis = {
        "(" : ")",
        "{":"}",
        "[":"]"
    }

    stack = []
    for ch in s:
        if ch in pair_paranthesis.keys():
            stack.append(ch)
            #print(stack)

        else:
            if not stack:
                return False
            else:
                #print(stack)
                #print(ch)
                peek_parenthesis = stack.pop()
                #print(peek_parenthesis)
                if pair_paranthesis[peek_parenthesis] != ch:
                    return False
    if stack:
        return False
    return True



print(isValid("{[]})"))
        
        
        

