from HashTable import HashTable

class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.identifiersHashTable = HashTable(size)
        self.intConstantsHashTable = HashTable(size)
        self.stringConstantsHashTable = HashTable(size)

    def addIdentifier(self, name):
        return self.identifiersHashTable.add(name)

    def addIntConstant(self, constant):
        return self.intConstantsHashTable.add(constant)

    def addStringConstant(self, constant):
        return self.stringConstantsHashTable.add(constant)

    def hasIdentifier(self, name):
        return self.identifiersHashTable.contains(name)

    def hasIntConstant(self, constant):
        return self.intConstantsHashTable.contains(constant)

    def hasStringConstant(self, constant):
        return self.stringConstantsHashTable.contains(constant)

    def getPositionIdentifier(self, name):
        return self.identifiersHashTable.getPosition(name)

    def getPositionIntConstant(self, constant):
        return self.intConstantsHashTable.getPosition(constant)

    def getPositionStringConstant(self, constant):
        return self.stringConstantsHashTable.getPosition(constant)

    def __str__(self):
        return f"SymbolTable{{identifiersHashTable={self.identifiersHashTable}\nintConstantsHashTable={self.intConstantsHashTable}\nstringConstantsHashTable={self.stringConstantsHashTable}"
