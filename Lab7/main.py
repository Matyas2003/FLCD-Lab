class Node:
    def __init__(self, val):
        self.value = val
        self.children = []
        self.parent = None
        self.index = 0

class Config:
    def __init__(self, state, length, working_stack, input_stack):
        self.state = state
        self.length = length
        self.working_stack = working_stack
        self.input_stack = input_stack
        self.symbol_count = {}

def print_tree(root, depth=0):
    # Recursive function to print the tree with proper indentation
    if root:
        print("  " * depth + str(root.value))
        for c in root.children:
            print_tree(c, depth + 1)


def create_parent_sibling_table(root):
    if root is None:
        return

    q = [[root, 0, 0]]
    table = []
    index = 1
    while len(q) != 0:
        n = len(q)
        while n > 0:
            p = q[0]
            q.pop(0)
            table.append([p[0].value, p[1], p[2]])
            for i in range(len(p[0].children)):
                if i == 0:
                    q.append([p[0].children[i], len(table), 0])
                else:
                    q.append([p[0].children[i], len(table), index])
                index += 1
            n -= 1
    return table


class ParserOutput:
    def __init__(self, str_of_production, root):
        self.prod = str_of_production
        self.root = Node(root)

    def create_tree(self):
        i = 2
        current_node = self.root
        current_node.index = int(self.prod[1])
        while i < len(self.prod):
            next_node = Node(self.prod[i])
            # non terminal
            if self.prod[i] in grammar.nonterminals:
                current_node.children.append(next_node)
                next_node.parent = current_node
                next_node.index = int(self.prod[i + 1])
                current_node = next_node
                i += 2
            # terminal and done
            elif self.prod[i] in grammar.productions[current_node.value][current_node.index - 1]:
                current_node.children.append(next_node)
                next_node.parent = current_node
                i += 1
            else:
                # terminal and up
                while self.prod[i] not in grammar.productions[current_node.value][current_node.index - 1]:
                    current_node = current_node.parent
                current_node.children.append(next_node)
                i += 1
        print_tree(self.root)

class Grammar:
    def __init__(self):
        self.nonterminals = []
        self.terminals = []
        self.start_symbol = ""
        self.productions = dict()
        self.cfg = True

    def read_from_file(self, file):
        f = open(file, 'r')
        lines = f.readlines()

        nont = lines[0]
        nont = nont.split(" ")
        nont[len(nont) - 1] = nont[len(nont) - 1].replace("\n", "")
        self.nonterminals = nont

        term = lines[1]
        term = term.split(" ")
        term[len(term) - 1] = term[len(term) - 1].replace("\n", "")
        self.terminals = term

        self.start_symbol = lines[2].replace("\n", "")

        for i in range(3, len(lines)):
            line = lines[i].split("->")
            left = line[0].split(",")
            if len(left) > 1 or left[0] not in self.nonterminals:
                self.cfg = False
            right = line[1].replace("\n", "").split("|")
            for l in left:
                if l in self.productions:
                    new_right = self.productions.get(l)
                    for r in right:
                        if r == "Îµ":
                            r = "ε"
                        new_right.append(r)
                    self.productions[l] = new_right
                else:
                    new_right = []
                    for r in right:
                        if r == "Îµ":
                            r = "ε"
                        new_right.append(r)
                    self.productions[l] = new_right

    def print_nonterminals(self):
        str = ""
        for nont in self.nonterminals:
            str += nont + ","
        str = str[:-1]
        print("N={", str, "}")

    def print_terminals(self):
        str = ""
        for term in self.terminals:
            str += term + ","
        str = str[:-1]
        print("Σ={", str, "}")

    def print_start_symbol(self):
        print("Starting symbol:", self.start_symbol)

    def print_productions(self):
        str = ""
        for prod in self.productions:
            right = ""
            for r in self.productions[prod]:
                right += r + "|"
            right = right[:-1]
            str += prod + "->" + right + ","
        str = str[:-1]
        print("P={", str, "}")

    def print_prod_for_nonterm(self, nonterm):
        if nonterm not in self.productions:
            print("Nonexistent nonterminal")
            return
        right = ""
        for r in self.productions[nonterm]:
            right += r + "|"
        right = right[:-1]
        print(nonterm + "->" + right)

    def cfg_check(self):
        if self.cfg:
            print("True")
        else:
            print("False")


def remaining_input_head(remaining_input):
    return remaining_input[0]


def parsed_input_head(parsed_input):
    if parsed_input[len(parsed_input) - 1].isnumeric():
        return parsed_input[len(parsed_input) - 2]
    else:
        return parsed_input[len(parsed_input) - 1]


def expand(config):
    global grammar
    symbol_count = config.symbol_count.get(config.input_stack[0], 0) + 1
    parsed_input = config.working_stack + config.input_stack[0] + str(symbol_count)
    remaining_input_str = "".join(config.input_stack[1:])
    remaining_input = grammar.productions[config.input_stack[0]][0] + remaining_input_str
    config.working_stack = parsed_input
    config.input_stack = remaining_input
    config.symbol_count[config.input_stack[0]] = symbol_count
    return config


def advance(config):
    global grammar
    config.length += 1
    parsed_input = config.working_stack + config.input_stack[0]
    remaining_input = config.input_stack[1:]
    config.working_stack = parsed_input
    config.input_stack = remaining_input
    return config


def momentary_insuccess(config):
    config.state = "back state"
    return config


def back(config):
    # take parsed_input and reverse it
    parsed_input_aux = config.working_stack[::-1]
    head = parsed_input_head(config.working_stack)
    # delete the head (including the index)
    split_parsed_input = parsed_input_aux.split(head, 1)
    # reverse the string -> initial string - the head
    parsed_input_aux = split_parsed_input[1][::-1]

    config.length = config.length - 1
    config.working_stack = parsed_input_aux
    config.input_stack = head + config.input_stack

    return config


def another_try(config):
    head = parsed_input_head(config.working_stack)

    if config.length == 1 and head == grammar.start_symbol:
        config.state = 'error state'
    else:
        current_nonterminal_index = int(config.working_stack[len(config.working_stack) - 1])
        productions = grammar.productions[head]
        if len(productions) > current_nonterminal_index:  # then there is a production for the head non-terminal
            current_production = productions[current_nonterminal_index]
            old_production = productions[current_nonterminal_index - 1]
            new_parsed_input = config.working_stack[:-2] + head + str(current_nonterminal_index + 1)
            new_remaining_input = current_production + config.input_stack[len(old_production):]

            config.state = 'normal state'
            config.working_stack = new_parsed_input
            config.input_stack = new_remaining_input

        else:  # there isn't a production for the head non-terminal
            old_production = productions[current_nonterminal_index - 1]

            config.state = 'back state'
            config.working_stack = config.working_stack[:-2]
            config.input_stack = head + config.input_stack[len(old_production):]

    return config


def success(config):
    config.state = "final state"
    return config


def is_empty(remaining_input):
    if len(remaining_input) == 0:
        return True
    else:
        return False


def print_result_table(table):

    for i in range(len(table)):
        print(str(i+1), ":", table[i])


def write_table_to_file(table):
    file_name = "out1.txt"
    f = open(file_name, "w")
    for i in range(len(table)):
        f.write(str(i+1) + " : " + table[i].__str__() + "\n")


def build_string_of_production(prod):
    parser = ParserOutput(prod, prod[0])
    parser.create_tree()
    result_table = create_parent_sibling_table(parser.root)
    print_result_table(result_table)
    write_table_to_file(result_table)


def rd_parser():
    global grammar, word
    q = "normal state"
    b = "back state"
    f = "final state"
    e = "error state"
    config = Config(q, 1, "", "S")
    while config.state != f and config.state != e:
        if config.state == q:
            if config.length == len(word) + 1 and is_empty(config.input_stack):
                config = success(config)
            else:
                if remaining_input_head(config.input_stack) in grammar.nonterminals:
                    config = expand(config)
                else:
                    if config.length <= len(word) and remaining_input_head(config.input_stack) == word[config.length - 1]:
                        config = advance(config)
                    else:
                        config = momentary_insuccess(config)
        else:
            if config.state == b:
                if parsed_input_head(config.working_stack) in grammar.terminals:
                    config = back(config)
                else:
                    config = another_try(config)
    if config.state == e:
        print("Error")
    else:
        print("Sequence accepted")
        build_string_of_production(config.working_stack)


def read_sequence():
    f = open("seq.txt", 'r')
    return f.readline()

grammar = Grammar()
def menu():
    print("_____MENU_____")
    print("0. Exit")
    print("1. Read grammar from file")
    print("2. Print set of nonterminals")
    print("3. Print set of terminals")
    print("4. Print starting symbol")
    print("5. Print set of productions")
    print("6. Print productions for a given nonterminal")
    print("7. CFG check")
    print("8. Recursive descent parser")
    print("9. Recursive descent parser - prepared example")


if __name__ == '__main__':
    while True:
        menu()
        cmd = int(input("command >>> "))
        if cmd == 0:
            exit()
        if cmd == 1:
            file_name = input("file name >>> ")
            grammar.read_from_file(file_name)
        if cmd == 2:
            grammar.print_nonterminals()
        if cmd == 3:
            grammar.print_terminals()
        if cmd == 4:
            grammar.print_start_symbol()
        if cmd == 5:
            grammar.print_productions()
        if cmd == 6:
            nonterm = input("given non-terminal >>> ")
            grammar.print_prod_for_nonterm(nonterm)
        if cmd == 7:
            grammar.cfg_check()
        if cmd == 8:
            word = input("given word to verify >>> ")
            rd_parser()
        if cmd == 9:
            grammar.read_from_file("g1.txt")
            word = read_sequence()
            rd_parser()