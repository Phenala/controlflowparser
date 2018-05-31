from blockmap import BlockMap


class Mapper:

    def __init__(self, blockset):
        self.blockSet = blockset
        self.paths = []

    def buildPaths(self):
        self.initPaths()
        while not self.isMapComplete():
            self.iteratePaths()

    def initPaths(self):
        startBlockMap = BlockMap(self.blockSet.startBlock)
        self.paths.append([startBlockMap])

    def iteratePaths(self):
        for path in self.paths:
            lastBlockMap = path[-1]
            if lastBlockMap.block.isCondBlock:
                self.handleConditionalBlockMap(path)
            if lastBlockMap.block.isProcessBlock:
                self.handleProcessBlockMap(path)

    def handleConditionalBlockMap(self, path):
        truePath = path
        trueBlockMap = truePath[-1]
        falsePath = path.copy()
        falseBlockMap = BlockMap(falsePath[-1].block)
        falsePath = falsePath[:-1]
        falsePath.append(falseBlockMap)
        self.paths.insert(self.paths.index(path) + 1, falsePath)
        
        trueBlockMap.condSolution = True
        falseBlockMap.condSolution = False
        
        truePath.append(BlockMap(trueBlockMap.block.trueBlock))
        falsePath.append(BlockMap(falseBlockMap.block.falseBlock))

    def handleProcessBlockMap(self, path):
        if path[-1].block == self.blockSet.endBlock:
            return
        nextBlock = path[-1].block.nextBlock
        nextBlockMap = BlockMap(nextBlock)
        path.append(nextBlockMap)

    def isMapComplete(self):
        for path in self.paths:
            if path[-1].block != self.blockSet.endBlock:
                return False
        return True

    def printMap(self):
        print("The program has",len(self.paths),"possible paths.\n")
        counter = 1
        for path in self.paths:
            pathString = self.printPath(path)
            print(str(counter) + ". " + pathString)
            print()
            counter += 1

    def printPath(self, path):
        out = ""
        for blockMap in path:
            out += blockMap.print()
        return out
               
