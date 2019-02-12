import pyperclip

def stringConcat(splitBy='\n', joinBy=', ', wrapBy="'"):
    inputString = pyperclip.paste()
    arr = inputString.split(splitBy)

    outputString = ''

    for s in arr:
        if len(s) > 0:
            outputString+=("{wrap}{element}{wrap}{join}"
                           .format(wrap=wrapBy, element=s, join=joinBy))
    if len(outputString) > 0:
        outputString=outputString[:-2]

    pyperclip.copy(outputString)

if __name__ == '__main__':
    stringConcat()
