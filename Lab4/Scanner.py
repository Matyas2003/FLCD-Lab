import re
from SymbolTable import SymbolTable


class Scanner:
    def __init__(self):
        self.program = ""
        self.tokens = []
        self.reserved_words = []
        self.symbol_table = SymbolTable(47)
        self.PIF = []
        self.index = 0
        self.printable_index = 0
        self.current_line = 1

        try:
            self.read_tokens()
        except Exception as e:
            print(e)

    def set_program(self, program):
        self.program = program

    def read_tokens(self):
        try:
            with open("Token.in", "r") as file:
                lines = file.read().splitlines()
                for line in lines:
                    parts = line.split(" ")
                    if parts[0] in ["and", "bool", "str", "character", "constant", "do", "else", "float", "for", "if",
                                    "integer", "in", "or", "out", "read", "string", "sqrt", "then", "while", "write"]:
                        self.reserved_words.append(parts[0])
                    else:
                        self.tokens.append(parts[0])
        except FileNotFoundError:
            raise Exception("Token file not found")

    def skip_spaces(self):
        while self.index < len(self.program) and self.program[self.index].isspace():
            if self.program[self.index] == '\n':
                self.current_line += 1
                self.printable_index = 0
            self.index += 1
            self.printable_index += 1

    def skip_comments(self):
        while self.index < len(self.program) and self.program[self.index] == '#':
            while self.index < len(self.program) and self.program[self.index] != '\n':
                self.index += 1
                self.printable_index += 1

    def treat_string_constant(self):
        regex_for_string_constant = re.compile(r'"[^"]*"')
        match = regex_for_string_constant.search(self.program[self.index-1:])
        if not match:
            if re.compile(r'"[^"]"').search(self.program[self.index:]):
                raise Exception("Invalid string constant at line " + str(self.current_line))
            if re.compile(r'"[^"]*').search(self.program[self.index:]):
                raise Exception("Missing \" at line " + str(self.current_line) + ", index " + str(self.printable_index))
            return False

        string_constant = match.group(0)
        self.index += len(string_constant)
        self.printable_index += len(string_constant)
        try:
            position = self.symbol_table.add_string_constant(string_constant)
        except Exception:
            position = self.symbol_table.get_position_string_constant(string_constant)
        self.PIF.append((f"str constant {string_constant}", position))
        return True

    def treat_int_constant(self):
        regex_for_int_constant = re.compile(r'^([+-]?[1-9][0-9]*|0)')
        match = regex_for_int_constant.search(self.program[self.index:])
        if not match:
            return False

        if re.compile(r'^([+-]?[1-9][0-9]*|0)[a-zA-Z_]').search(self.program[self.index:]):
            return False

        int_constant = match.group(1)
        self.index += len(int_constant)
        self.printable_index += len(int_constant)
        try:
            position = self.symbol_table.add_int_constant(int(int_constant))
        except Exception:
            position = self.symbol_table.get_position_int_constant(int(int_constant))
        self.PIF.append((f"int constant {int_constant}", position))
        return True

    def check_if_valid(self, possible_identifier, program_substring):
        if possible_identifier in self.reserved_words:
            return False
        if re.search(r"^([A-Za-z_][A-Za-z0-9_]*, )*([A-Za-z_][A-Za-z0-9_]*) -> (integer|character|string|float)", program_substring):
            return True
        return self.symbol_table.has_identifier(possible_identifier)

    def treat_identifier(self):
        regex_for_identifier = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*')
        match = regex_for_identifier.search(self.program[self.index:])
        if not match:
            return False

        identifier = match.group(0)
        if not self.check_if_valid(identifier, self.program[self.index:]):
            return False
        self.index += len(identifier)
        self.printable_index += len(identifier)

        try:
            position = self.symbol_table.add_identifier(identifier)
        except Exception:
            position = self.symbol_table.get_position_identifier(identifier)
        self.PIF.append((f"identifier {identifier}", position))
        return True

    def treat_from_token_list(self):
        possible_token = self.program[self.index:].split(" ")[0]
        for reserved_token in self.reserved_words:
            if possible_token.startswith(reserved_token):
                regex = r"^" + "[a-zA-Z0-9_]*" + reserved_token + r"[a-zA-Z0-9_]+"
                if re.search(regex, possible_token):
                    return False
                self.index += len(reserved_token)
                self.printable_index += len(reserved_token)
                self.PIF.append((reserved_token, (-1, -1)))
                return True
        for token in self.tokens:
            if token == possible_token:
                self.index += len(token)
                self.printable_index += len(token)
                self.PIF.append((token, (-1, -1)))
                return True
            elif possible_token.startswith(token):
                self.index += len(token)
                self.printable_index += len(token)
                self.PIF.append((token, (-1, -1)))
                return True
        return False

    def next_token(self):
        self.skip_spaces()
        self.skip_comments()
        if self.index == len(self.program):
            return
        if self.treat_identifier():
            return
        if self.treat_int_constant():
            return
        if self.treat_from_token_list():
            return
        if self.treat_string_constant():
            return
        raise Exception("Lexical error: invalid token at line " + str(self.current_line) + ", index " + str(self.printable_index))

    def scan(self, program_file_name):
        try:
            with open("lab1/" + program_file_name, "r") as file:
                print("Now scanning ", program_file_name)
                self.set_program(file.read())
                self.index = 0
                self.printable_index = 0
                self.PIF = []
                self.symbol_table = SymbolTable(47)
                self.current_line = 1
                while self.index < len(self.program):
                    self.next_token()

            with open("PIF_" + program_file_name.replace(".txt", ".out"), "w") as file_writer:
                for pair in self.PIF:
                    file_writer.write(pair[0] + " -> (" + str(pair[1][0]) + ", " + str(pair[1][1]) + ")\n")

            with open("ST_" + program_file_name.replace(".txt", ".out"), "w") as file_writer:
                file_writer.write(self.symbol_table.__str__())

            print("Lexically correct")

        except (FileNotFoundError, Exception) as e:
            print(str(e))
