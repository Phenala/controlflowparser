      
class BlockMap:

    def __init__(self, block):
        self.block = block
        self.condSolution = None

    def print(self):
        string = ""
        if self.block.code[0].lower() == "start":
            return "Start ---> "
        if self.block.code[0].lower() == "end":
            return "End"
        codeString = str(self.block.code)
        if len(self.block.code) == 1:
            codeString = self.block.code[0]
        string += codeString
        if self.condSolution != None:
            if self.condSolution:
                string += "(T)"
            else:
                string += "(F)"
        string += " ---> "
        return string
