def push(stack,item):
    stack.append(item)

def pop(stack):
    if isEmpty(stack):
        return "Stack is empty"
    else:
        return stack.pop()

def peek(stack):
    if isEmpty(stack):
        return "Stack is empty"
    else:
        return stack[-1]    


def isEmpty(stack):
    return len(stack)==0

stack = []
push(stack, "a")
push(stack, "b")
push(stack, "c")
push(stack, "d")
push(stack, "e")

print(stack)

print(peek(stack))

print(pop(stack))