class Node:
    def __init__(self, val):
        self.value = val
        self.children = []
        self.parent = None
        self.index = 0


def print_tree(root):
    # preorder print
    if root:
        print(root.value)
        for c in root.children:
            print_tree(c)


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


def beta_head(beta):
    return beta[0]


def alpha_head(alpha):
    if alpha[len(alpha) - 1].isnumeric():
        return alpha[len(alpha) - 2]
    else:
        return alpha[len(alpha) - 1]


def expand(config):
    global grammar
    alpha = config[2] + config[3][0] + "1"
    beta_str = ""
    for i in range(1, len(config[3])):
        beta_str += config[3][i]
    beta = grammar.productions[config[3][0]][0] + beta_str
    config[2] = alpha
    config[3] = beta
    return config


def advance(config):
    global grammar
    config[1] += 1
    alpha = config[2] + config[3][0]
    beta = config[3][1:]
    config[2] = alpha
    config[3] = beta
    return config


def momentary_insuccess(config):
    config[0] = "back state"
    return config


def back(config):
    # take alpha and reverse it
    alpha_aux = config[2][::-1]
    head = alpha_head(config[2])
    # delete the head (including the index)
    split_alpha = alpha_aux.split(head, 1)
    # reverse the string -> initial string - the head
    alpha_aux = split_alpha[1][::-1]

    config[1] = config[1] - 1
    config[2] = alpha_aux
    config[3] = head + config[3]

    return config


def another_try(config):
    head = alpha_head(config[2])

    if config[1] == 1 and head == grammar.start_symbol:
        config[0] = 'error state'
    else:
        current_nonterminal_index = int(config[2][len(config[2]) - 1])
        productions = grammar.productions[head]
        if len(productions) > current_nonterminal_index:  # then there is a production for the head non-terminal
            current_production = productions[current_nonterminal_index]
            old_production = productions[current_nonterminal_index - 1]
            new_alpha = config[2][:-2] + head + str(current_nonterminal_index + 1)
            new_beta = current_production + config[3][len(old_production):]

            config[0] = 'normal state'
            config[2] = new_alpha
            config[3] = new_beta

        else:  # there isn't a production for the head non-terminal
            old_production = productions[current_nonterminal_index - 1]

            config[0] = 'back state'
            config[2] = config[2][:-2]
            config[3] = head + config[3][len(old_production):]

    return config


def success(config):
    config[0] = "final state"
    return config


def is_empty(beta):
    if len(beta) == 0:
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
    config = [q, 1, "", "S"]
    while config[0] != f and config[0] != e:
        if config[0] == q:
            if config[1] == len(word) + 1 and is_empty(config[3]):
                config = success(config)
            else:
                if beta_head(config[3]) in grammar.nonterminals:
                    config = expand(config)
                else:
                    if config[1] <= len(word) and beta_head(config[3]) == word[config[1] - 1]:
                        config = advance(config)
                    else:
                        config = momentary_insuccess(config)
        else:
            if config[0] == b:
                if alpha_head(config[2]) in grammar.terminals:
                    config = back(config)
                else:
                    config = another_try(config)
    if config[0] == e:
        print("Error")
    else:
        print("Sequence accepted")
        build_string_of_production(config[2])


def read_sequence():
    f = open("seq.txt", 'r')
    return f.readline()


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
    grammar = Grammar()
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