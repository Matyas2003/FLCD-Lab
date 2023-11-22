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
        nont[len(nont)-1] = nont[len(nont)-1].replace("\n", "")
        self.nonterminals = nont

        term = lines[1]
        term = term.split(" ")
        term[len(term)-1] = term[len(term)-1].replace("\n", "")
        self.terminals = term

        self.start_symbol = lines[2].replace("\n", "")

        for i in range(3, len(lines)):
            line = lines[i].split("->")
            left = line[0].split(",")
            # print(left, "\n")
            if len(left) > 1 or left[0] not in self.nonterminals:
                # print("wut ", left, self.nonterminals)
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
            nonterm = input("given nonterminal >>> ")
            grammar.print_prod_for_nonterm(nonterm)
        if cmd == 7:
            grammar.cfg_check()