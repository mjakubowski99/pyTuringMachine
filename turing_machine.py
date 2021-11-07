from Parser.FileDataParser import FileDataParser

def printMachine(word, index, state):
    word = "".join(word)

    fillSpaces = ""
    for x in range(0, index+4):
        fillSpaces += " "

    print(fillSpaces[:-1]+"| stan: "+state)
    print("___"+word+"___")

def genReport(description, startWord, endWord, endState):
    file = open("report.txt", "w")
    file.write("""{}
Slowo poczatkowe: {}
Slowo koncowe: {}
Osiagniety stan: {}
""".format(description, startWord, endWord, endState) )


class TuringMachine:

    def __init__(self, data: FileDataParser):
        self.data = data
        self.beginWord = self.data.word
        self.data.word = list(self.data.word)
        self.index = 1

    def step(self, state):
        symbol = self.data.word[self.index]
        if( state in self.data.instructions.keys() ):
            instructions = self.data.instructions[state][symbol]
        else:
            print("Procedura zakonczona brak zdefiniowanych operacji")
            genReport("Błąd! Brak zdefiniowanych operacji!", self.beginWord, "".join(self.data.word), state)
            exit()
        

        state = instructions['state']

        self.data.word[self.index] = instructions['symbol']

        if( instructions['move'] == "r" ):
            self.index += 1
        elif( instructions['move'] == "l" ):
            self.index -= 1
        elif( instructions['move'] == "s" ):
            pass
        else:
            raise ValueError("Bad instruction")

        
        if( self.index < 0 ):
            self.index = 0 

        if( self.index >= len(self.data.word) ):
            self.index = len(self.data.word)-1

        printMachine(self.data.word, self.index, state)

        return state 

    def simulate(self):
        state  = self.data.beginState
        loopCounter = 0
        print("Begin: ")
        printMachine(self.data.word, self.index, state)

        lenWord = len(self.data.word)
        
        while True:
            state = self.step(state)
            if( state in self.data.endState ):
                genReport(self.data.description, self.beginWord, "".join(self.data.word), state)
                print("Stan końcowy osiągnięty. Procedura zakończona")
                exit(0)
            loopCounter+=1

            if( loopCounter > 1000 * lenWord ):
                print("W stanie {} jest prawdopodobnie błąd".format(state) )
                print("Maszyna nie może osiągnąć stanu końcowego")
                genReport("Błąd! Maszyna się zapętliła!", self.beginWord, "".join(self.data.word), state)
                break 
            

def main():
    file = open("dane1.txt")
    data = FileDataParser(file)

    machine = TuringMachine(data)
    machine.simulate()


main()