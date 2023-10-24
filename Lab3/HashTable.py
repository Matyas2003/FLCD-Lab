from typing import List, Tuple
from collections import defaultdict


class HashTable:
    def __init__(self, size):
        self.size = size
        self.items = [defaultdict(list) for _ in range(size)]

    def getSize(self):
        return self.size

    def hash(self, key):
        return key % self.size if isinstance(key, int) else sum(ord(char) for char in key) % self.size

    def getHashValue(self, key):
        if isinstance(key, int):
            return self.hash(key)
        elif isinstance(key, str):
            return self.hash(key)

    def add(self, key):
        hashValue = self.getHashValue(key)
        if key not in self.items[hashValue][key]:
            self.items[hashValue][key] = key
            return (hashValue, list(self.items[hashValue].values()).index(key))
        raise Exception(f"Key {key} is already in the table!")

    def contains(self, key):
        hashValue = self.getHashValue(key)
        return key in self.items[hashValue]

    def getPosition(self, key):
        if self.contains(key):
            hashValue = self.getHashValue(key)
            return (hashValue, list(self.items[hashValue].values()).index(key))
        return (-1, -1)

    def __str__(self):
        return f"HashTable{self.items}"
