from Scanner import Scanner

def main():
    scanner = Scanner()
    program1 = "p1.txt"
    program2 = "p2.txt"
    program3 = "p3.txt"
    program1err = "p1err.txt"
    scanner.scan(program1)
    scanner.scan(program2)
    scanner.scan(program3)
    scanner.scan(program1err)
if __name__ == "__main__":
    main()