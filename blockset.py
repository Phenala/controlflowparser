from block import Block


class BlockSet:

    def __init__(self):

        self.handlers = [self.handleIfStatement, self.handleElseStatement, self.handleElseIfStatement, self.handleProcessStatement]
        self.startBlock = None
        self.endBlock = None
        self.stack = []
        self.waitstack = []
        self.currentBlock = None

    def initBlockSet(self):
        
        self.currentBlock = Block()
        self.currentBlock.addCode("Start")
        self.currentBlock.isProcessBlock = True
        self.currentBlock.flagBlock = True
        self.startBlock = self.currentBlock
        self.newBlock()
        self.getLastBlock().setNextBlock(self.currentBlock)

    def build(self, lines):

        self.initBlockSet()
        for line in lines:
            if line.strip() != "":
                self.analyzeLine(line)

        self.finalizeBlockSet()
        self.stack[1].defineBlock()

    def analyzeLine(self, line):

        lineDepth = self.checkDepth(line)
        #print(lineDepth, self.getLastBlock().depth, self.getLastBlock().code)
        self.printStack()
        self.topurge = lineDepth < self.getLastBlock().depth
        
        for handler in self.handlers:
            if handler(line):
                break

        if self.topurge:
            #print("ancestor code is", self.getAncestorAt(lineDepth).code)
            self.getAncestorAt(lineDepth).purgeToBlock(self.getLastBlock())


    def handleIfStatement(self, line):
        
        if line.strip().startswith("if "):
            self.currentBlock.checkDepth(line)
            #print("Added if block")
            self.currentBlock.addCode(line)
            self.newBlock()
            self.getLastBlock().setTrueBlock(self.currentBlock)
            #print("set true of block", self.getLastBlock().code)
            return True

    def handleElseStatement(self, line):

        if line.strip().startswith("else:"):
            self.currentBlock.checkDepth(line)
            #print("Added else block of ",self.getFreeElseAncestor(self.currentBlock).code,'to', self.currentBlock.code)
            self.getLastBlock().detachBlock(self.currentBlock)
            self.topurge = False
            self.getFreeElseAncestor(self.currentBlock).setFalseBlock(self.currentBlock)
            self.newBlock()
            self.getLastBlock().isProcessBlock = True
            return True

    def handleElseIfStatement(self, line):

        if line.strip().startswith("elif "):
            self.currentBlock.checkDepth(line)
            #print("Added elif block")
            self.getLastBlock().detachBlock(self.currentBlock)
            self.topurge = False
            self.getFreeElseAncestor(self.currentBlock).setFalseBlock(self.currentBlock)
            self.currentBlock.addCode(line)
            self.newBlock()
            self.getLastBlock().setTrueBlock(self.currentBlock)
            self.getLastBlock().ancestorSkip = True
            return True

    def handleProcessStatement(self, line):

        if self.getLastBlock().isProcessBlock and not self.topurge and not self.getLastBlock().flagBlock:
            #print("Added code to process block")
            self.getLastBlock().addCode(line)
        else:
            #print("Added process block")
            self.currentBlock.addCode(line)
            self.newBlock()
            self.getLastBlock().setNextBlock(self.currentBlock)

    def finalizeBlockSet(self):
        self.currentBlock.addCode("End")
        self.stack[0].purgeToBlock(self.currentBlock)
        self.currentBlock.flagBlock = True
        self.endBlock = self.currentBlock

    def printStack(self):
        g = [i.code for i in self.stack]
        #print(g)
            

    def checkDepth(self, line):
        
        depth = 0
        while line.find('\t') != -1:
            line = line[1:]
            depth += 1
        return depth

    def truncateStackTo(self, parentBlock):
        while self.getLastBlock() != parentBlock:
            self.stack.pop()

    def getAncestorAt(self, depth):
        stack = self.stack.copy()
        last = stack.pop()
        last = stack.pop()
        while last.depth > depth:
            last = stack.pop()
            if last.ancestorSkip:
                last = stack.pop()
            
        return last

    def getFreeElseAncestor(self, block):
        stack = self.stack.copy()
        last = stack.pop()
        while not (last.depth == block.depth and last.isCondBlock and last.falseBlock == None):
            last = stack.pop()

        #print("Retrieved a free else ancestor of ", last.code, "of block depth", block.depth)
        return last
        

    def newBlock(self):
        self.stack.append(self.currentBlock)
        tmpBlock = self.currentBlock
        self.currentBlock = Block()
        self.currentBlock.parentBlock = tmpBlock

    def isolateConditionStatement(self, line):
        nline = line.replace("if ", "").replace("elif ", "").replace(":", "")
        return nline

    def getLastBlock(self):
        
        return self.stack[-1]
