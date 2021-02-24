import pyperclip

perLineCount = 6

def stringConcat(splitBy='\n', joinBy=', ', wrapBy="'"):
    inputString = pyperclip.paste()
    arr = inputString.split(splitBy)

    outputString = ''
    counter = 0
    for s in arr:
        if len(s) > 0:
            outputString+=("{wrap}{element}{wrap}{join}"
                           .format(wrap=wrapBy, element=s.strip(), join=joinBy))
        counter += 1
        if perLineCount > 0:
            if counter % perLineCount == 0:
                outputString += '\n'
    pyperclip.copy(outputString)

if __name__ == '__main__':
    stringConcat()
    print('Concated string copied to clipboard')
    
