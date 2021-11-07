import json 

class FileDataParser():

    def __init__(self, file):
        self.file = file
        self.parse()

    def baseParse(self, name):
        line = self.file.readline()
        if( len(line) == 0 ):
            raise ValueError("Bad file format") 

        data = line.split(':')

        if( len(data) < 2 ):
            raise ValueError("Data is not valid")

        if( data[0] != name ):
            raise ValueError("Not valid header") 

        return data 

    def parseToArray(self, name):
        data = self.baseParse(name)

        return data[1][1:-1].split(',')
        
    def parseToStr(self, name):
        data = self.baseParse(name)
        
        return data[1][1:-1]

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
                self.instructions[line.split(':')[0]] = {}
                last_index = line.split(':')[0]
            else:
                filtered = line.replace(' ', '')
                if( last_index == False ):
                    raise ValueError("Parsing error")

                key = filtered.split(';')[0]
                data = filtered.split(';')[1].split(',')
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
        self.endState = self.parseToStr("stan koncowy")
        self.beginState = self.parseToStr("stan poczatkowy")
        self.parseInstructions()

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