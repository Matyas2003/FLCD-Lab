class FA:

    def __init__(self):
        self.__input_file = ""
        self.__all_states = list()
        self.__input_symbols = list()
        self.__initial_state = None
        self.__final_states = list()
        self.__transition_function = dict()

    def get_input_file(self):
        return self.__input_file

    def get_all_states(self):
        return self.__all_states

    def get_input_symbols(self):
        return self.__input_symbols

    def get_initial_state(self):
        return self.__initial_state

    def get_final_states(self):
        return self.__final_states

    def get_transition_function(self):
        return self.__transition_function

    def read_from_file(self, input_file):
        self.__init__()
        
        with open(input_file) as file:
            self.__input_file = input_file
            
            lines = [line.replace(' ', '').strip() for line in file.readlines()]

            self.__parse_file(lines)

    def __parse_file(self, lines):
        self.__all_states = lines[0].split(',')
        self.__input_symbols = lines[1].split(',')
        self.__initial_state = lines[2]
        self.__final_states = lines[3].split(',')


        for line in lines[4:]:

            state = line[1]
            input_symbol = line[3]
            next_state = line[6]

            self.__transition_function[state, input_symbol] = next_state

    def seq_is_accepted(self, seq_list):
        curr_state = self.__initial_state

        for seq in seq_list:
            try:
                next_state = self.__transition_function[curr_state, seq]
            except KeyError:
                return False

            curr_state = next_state

        return curr_state in self.__final_states
