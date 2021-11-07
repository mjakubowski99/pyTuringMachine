import json 

class FileDataParser():

    def __init__(self, file):
        self.file = file
        self.parse()

    def baseParse(self, name):
        line = self.file.readline()

        #if no data from file found print bad file format
        if( len(line) == 0 ):
            raise ValueError("Bad file format") 

        data = line.split(':')

        if( len(data) < 2 ):
            raise ValueError("Data is not valid")

        #if header name is not valid raise error message
        if( data[0] != name ):
            raise ValueError("Not valid header") 

        return data 

    #convert parsed data to array
    def parseToArray(self, name):
        data = self.baseParse(name)

        return data[1][1:-1].split(',')
    
    #convert parsed data to str
    def parseToStr(self, name):
        data = self.baseParse(name)
        
        return data[1][1:-1]

    #parse instructions
    def parseInstructions(self):
        self.baseParse("instrukcja")

        self.instructions = {}
        last_index = False
        
        while True:
            line = self.file.readline()
            if( len(line) == 0 ):
                break 

            #it's letter
            if( line[0] != ' '):
                data = line.split(':')
                if(len(data)<1):
                    raise ValueError("Not valid state definition")
                
                self.instructions[data[0]] = {}
                last_index = data[0]
            else:
                filtered = line.replace(' ', '')
                if( last_index == False ):
                    raise ValueError("Parsing error")

                data = filtered.split(';')
                if(len(data)<2):
                    raise ValueError("Not valid instructions")

                key = data[0]
                data = data[1].split(',')

                if( len(data) < 3 ):
                    raise ValueError("Not valid instructions")

                self.instructions[last_index][key] = {
                    'state': data[0],
                    'symbol': data[1],
                    'move': data[2]
                }

    def parse(self):
        self.description = self.file.readline()[:-1]
        self.states = self.parseToArray("stany")
        self.alphabeth = self.parseToArray("alfabet")
        self.length = int( self.parseToStr("dlugosc slowa") )
        self.word = "_"+self.parseToStr("slowo")+"_"
        self.endState = self.parseToArray("stan koncowy")
        self.beginState = self.parseToStr("stan poczatkowy")
        self.parseInstructions()
        self.validate()

    #validate data to make sure that given state, symbols, and moves are valid
    def validate(self):
        for state in self.endState:
            if state not in self.states:
                raise ValueError("End state definiton is not valid")

        if self.beginState not in self.states:
            raise ValueError("Begin state is invalid")

        for char in self.word:
            if char not in self.alphabeth:
                raise ValueError("In word is char which is not in alphabeth")

        for key in self.instructions.keys():
            if key not in self.states:
                raise ValueError("State definiton is not valid")

        for (key,data) in self.instructions.items():
            if key not in self.states:
                raise ValueError("State definiton is not valid")

            for (key,instruction) in data.items():
                if key not in self.alphabeth:
                    raise ValueError("Instruction has invalid alphabeth symbol")

                if instruction["state"] not in self.states:
                    raise ValueError("State definiton is not valid")

                if instruction["symbol"] not in self.alphabeth:
                    raise ValueError("State definiton is not valid")

                if instruction["move"] not in ['r', 's', 'l']:
                    raise ValueError("Invalid move definiton")
        
    def __str__(self):
        return """
            {}
            stany: {}
            alfabet: {}
            długość słowa: {},
            słowo: {},
            stan końcowy: {}
            stan początkowy: {}
            instrukcje: {}
        """.format(
            self.description, str(self.states),
            str(self.alphabeth), self.length,
            self.word, self.endState,
            self.beginState, json.dumps( self.instructions )
        )