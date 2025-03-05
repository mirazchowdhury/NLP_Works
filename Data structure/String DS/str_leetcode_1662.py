def arrayStringsAreEqual(word1: list[str], word2: list[str]) -> bool:

    join1 = "".join(word1[0:len(word1)])
    join2 = "".join(word2[0:len(word2)])
    if join1 == join2:
        return "true"
    else: 
        return "false"
    
print(arrayStringsAreEqual(["a", "cb"],["ab", "c"]))
