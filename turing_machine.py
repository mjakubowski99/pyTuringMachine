from Parser.FileDataParser import FileDataParser

def printMachine(word, index, state):
    word = "".join(word)

    fillSpaces = ""
    for x in range(0, index+4):
        fillSpaces += " "

    print(fillSpaces[:-1]+"| stan: "+state)
    print("___"+word+"___")

class TuringMachine:

    def __init__(self, data):
        self.data = data
        self.data.word =  list(self.data.word)
        self.index = 1

    def step(self, state):
        symbol = self.data.word[self.index]
        if( state in self.data.instructions.keys() ):
            instructions = self.data.instructions[state][symbol]
        else:
            print("Procedura zakonczona brak zdefiniowanych operacji")
            exit()
        

        state = instructions[0]

        self.data.word[self.index] = instructions[2]

        if( instructions[4] == "r" ):
            self.index += 1
        elif( instructions[4] == "l" ):
            self.index -= 1
        elif( instructions[4] == "s" ):
            pass
        else:
            raise ValueError("Bad instruction")

        
        if( self.index < 0 ):
            self.index = 0 

        if( self.index >= len(self.data.word) ):
            self.index = len(self.data.word)-1

        printMachine(self.data.word, self.index, state)
        
        if( state == self.data.endState ):
            print("Stan końcowy osiągnięty. Procedura zakończona")
            exit(0)

        return state 

    def simulate(self):
        state  = self.data.beginState
        print("Begin: ")
        printMachine(self.data.word, self.index, state)
        
        input()
        while True:
            state = self.step(state)
            input()


def main():
    file = open("dane1.txt")
    data = FileDataParser(file)

    machine = TuringMachine(data)
    machine.simulate()

    

 


main()