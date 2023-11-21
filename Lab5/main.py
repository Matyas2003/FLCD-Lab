from FA import FA
import os

def show_menu():
    print("0 - Exit")
    print("1 - Read content from file")
    print("2 - Show FA content")
    print("3 - Test if sequence is accepted by the DFA")

def show_fa_content(fa):
    print(f"Set of input symbols: {fa.get_input_symbols()}")
    print(f"Set of all states: {fa.get_all_states()}")
    print(f"Initial state: {fa.get_initial_state()}")
    print(f"Set of final states: {fa.get_final_states()}")
    print(f"Transition function: {fa.get_transition_function()}")


def main():
    fa = FA()
    
    menu_option = None

    while menu_option != 0:
        show_menu()
        menu_option = int(input(">> "))
        os.system('cls')

        if menu_option == 1:
            print("Enter the input file name")
            file_name = input(">> ")
            os.system('cls')

            fa.read_from_file(file_name)


        if menu_option == 2:
            show_fa_content(fa)

            input("\nPress Enter to continue...")
            os.system('cls')

        if menu_option == 3:
            print("Enter the input sequence")
            seq = input(">> ")
            os.system('cls')

            result = fa.seq_is_accepted(seq)

            if result:
                print(f"The input sequence ({seq}) is accepted by the DFA")
            else:
                print(f"The input sequence ({seq}) is NOT accepted by the DFA")

            input("\nPress Enter to continue...")
            os.system('cls')

if __name__ == "__main__":
    main()