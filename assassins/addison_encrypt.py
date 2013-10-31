
import sys, string

def fibonacci(numIters):
    prevNum = 0
    thisNum = 1
    for i in range(numIters):
        temp = thisNum
        thisNum = prevNum + thisNum
        prevNum = temp
    return prevNum

def encrypt(s, KEY):
    ASCII = list(string.ascii_lowercase + "0123456789" + string.ascii_uppercase)
    result = ""
    total = sum(ASCII.index(char)  for char in s)
    keyTotal = sum(ASCII.index(KEY[i]) * i for i in range(len(KEY))) % len(ASCII)
    
    i = 0
    for char in s:
        index = ASCII.index(char) + keyTotal + i + fibonacci(keyTotal)
        if index > len(ASCII)-1:
            num = index / len(ASCII)
            index -= num *len(ASCII)
        result += ASCII[index]
        i+=1
    return result

def decrypt(s, KEY):
    ASCII = list(string.ascii_lowercase + "0123456789" + string.ascii_uppercase)
    result = ""
    keyTotal = sum(ASCII.index(KEY[i]) * i for i in range(len(KEY))) % len(ASCII)
        
    i = 0
    for char in s:
        index = ASCII.index(char) - keyTotal - i - fibonacci(keyTotal)
        if index < 0:
            index = index % len(ASCII)
        result += ASCII[index]
        i += 1
    return result
