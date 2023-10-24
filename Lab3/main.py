from SymbolTable import SymbolTable

def main():
    symbolTable = SymbolTable(42)
    p1 = (-1, -1)
    p2 = (-1, -1)
    p3 = (-1, -1)
    try:
        print(f"a -> {symbolTable.addIdentifier('a')}")
        print(f"b -> {symbolTable.addIdentifier('b')}")
        print(f"c -> {symbolTable.addIdentifier('c')}")
        p1 = symbolTable.addIdentifier("abc")
        print(f"abc -> {p1}")

        print(f"5 -> {symbolTable.addIntConstant(5)}")
        p2 = symbolTable.addIntConstant(100)
        print(f"100 -> {p2}")
        print(f"131 -> {symbolTable.addIntConstant(131)}")
        print(f"47 -> {symbolTable.addIntConstant(47)}")

        print(f"hi -> {symbolTable.addStringConstant('hi')}")
        p3 = symbolTable.addStringConstant("me")
        print(f"me -> {p3}")


        print(f"abc -> {symbolTable.addIdentifier('abc')}")
    except Exception as e:
        print(e)

    print(symbolTable)

    try:
        assert symbolTable.getPositionIdentifier("abc") == p1, f"abc does not have position {p1}"
        assert symbolTable.getPositionIntConstant(100) == p2, f"100 does not have position {p2}"
    except AssertionError as e:
        print(e)

    try:
        print(f"me -> {symbolTable.getPositionStringConstant('me')}")
        print(f"we change the value of p3 to (0, 2), so when we check if 'me' has the position of p3 we get")
        p3 = (0, 2)
        assert symbolTable.getPositionStringConstant('me') == p3, f"me does not have position {p3}"
    except AssertionError as e:
        print(e)

if __name__ == "__main__":
    main()