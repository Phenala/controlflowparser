from blockset import BlockSet
from mapper import Mapper

class Parser:

    def __init__(self, filepath):
        self.openFile(filepath)
        self.parseFile()

    def openFile(self, filepath):

        self.lines = open(filepath).readlines()

    def parseFile(self):
        
        self.blockSet = BlockSet()
        self.blockSet.build(self.lines)
        self.mapper = Mapper(self.blockSet)
        self.mapper.buildPaths()

    def showControlFlow(self):
        self.mapper.printMap()


