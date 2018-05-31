
class Block:

    def __init__(self, line = ""):

        self.code = []
        self.nextBlock = None
        self.trueBlock = None
        self.falseBlock = None
        self.parentBlock = None
        self.ancestorSkip = False
        self.flagBlock = False
        self.depth = 0
        self.isProcessBlock = False
        self.isCondBlock = False
        if line != "":
            self.addCode(line)

    def addCode(self, line):
        self.code.append(line.strip())
        self.checkDepth(line)

    def checkDepth(self, line):

        depth = 0
        while line.find('\t') != -1:
            line = line[1:]
            depth += 1
        self.depth = depth

    def hasUnaccountedBranch(self):
        return (self.isCondBlock and (self.trueBlock == None or self.falseBlock == None)) or (self.isProcessBlock and self.nextBlock == None)

    def purgeToBlock(self, block):
        if (block == self):
            return
        self.purgeConditional(block)
        self.purgeProcess(block)

    def purgeConditional(self, block):
        if self.isCondBlock:
            if self.trueBlock == None:
                self.trueBlock = block
                #print("purged true of",self.code,"to",block.code)
            else:
                self.trueBlock.purgeToBlock(block)
                
            if self.falseBlock == None:
                self.falseBlock = block
                #print("purged false of",self.code,"to",block.code)
            else:
                self.falseBlock.purgeToBlock(block)

    def purgeProcess(self, block):
        if self.isProcessBlock:
            if self.nextBlock == None:
                self.nextBlock = block
                #print("purged next of",self.code,"to",block.code)
            else:
                self.nextBlock.purgeToBlock(block)

    def detachBlock(self, block):
        if self.isProcessBlock:
            if self.nextBlock == block:
                self.nextBlock = None
        

    def setTrueBlock(self, block):

        self.isCondBlock = True
        self.trueBlock = block
        block.parent = self

    def setFalseBlock(self, block):

        self.isCondBlock = True
        self.falseBlock = block
        block.parent = self

    def defineBlock(self):
        if self.trueBlock or self.falseBlock:
            #print("Condition Block", str(self), ", True maps to", str(self.trueBlock), ", False maps to ", str(self.falseBlock))
            self.trueBlock.defineBlock()
            self.falseBlock.defineBlock()
        if self.nextBlock:
            #print("Process Block", str(self), ", Next maps to", str(self.nextBlock))
            self.nextBlock.defineBlock()
            
            

    def setNextBlock(self, block):

        self.isProcessBlock = True
        self.nextBlock = block
        block.parent = self

    def __str__(self):
        return str(self.depth) + "-" + str(self.code)
