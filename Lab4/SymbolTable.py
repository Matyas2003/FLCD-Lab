from HashTable import HashTable

class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.identifiers_hash_table = HashTable(size)
        self.int_constants_hash_table = HashTable(size)
        self.string_constants_hash_table = HashTable(size)

    def add_identifier(self, name):
        return self.identifiers_hash_table.add(name)

    def add_int_constant(self, constant):
        return self.int_constants_hash_table.add(constant)

    def add_string_constant(self, constant):
        return self.string_constants_hash_table.add(constant)

    def has_identifier(self, name):
        return self.identifiers_hash_table.contains(name)

    def has_int_constant(self, constant):
        return self.int_constants_hash_table.contains(constant)

    def has_string_constant(self, constant):
        return self.string_constants_hash_table.contains(constant)

    def get_position_identifier(self, name):
        return self.identifiers_hash_table.get_position(name)

    def get_position_int_constant(self, constant):
        return self.int_constants_hash_table.get_position(constant)

    def get_position_string_constant(self, constant):
        return self.string_constants_hash_table.get_position(constant)

    def __str__(self):
        table_str = "Symbol Table:\n"
        table_str += "{:<20} | {:<10}\n".format("Identifier", "Hash")
        table_str += "-" * 32 + "\n"

        for i in range(self.size):
            for identifier in self.identifiers_hash_table.items[i]:
                table_str += "{:<20} | {:<10}\n".format(identifier, i)

        table_str += "\n\n{:<20} | {:<10}\n".format("String Constant", "Hash")
        table_str += "-" * 32 + "\n"

        for i in range(self.size):
            for string_const in self.string_constants_hash_table.items[i]:
                table_str += "{:<20} | {:<10}\n".format(string_const, i)

        table_str += "\n\n{:<20} | {:<10}\n".format("Int Constant", "Hash")
        table_str += "-" * 32 + "\n"

        for i in range(self.size):
            for integer in self.int_constants_hash_table.items[i]:
                table_str += "{:<20} | {:<10}\n".format(integer, i)
        return table_str
