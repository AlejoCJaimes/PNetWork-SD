# Basic Class
class Transitions:
    def __init__(self, transition:str):
        self._transition = transition

class Places:
    def __init__(self, pname:str, tokens:int):
        self._pname = pname
        self._tokens = tokens

class Itransitions:
    def __init__(self, transitions:Transitions, places: Places, inputs: int):
        self._transitions = transitions
        self._places = places
        self._inputs = inputs

class Otransitions:
    def __init__(self, transitions:Transitions, places: Places, outputs: int):
        self._transitions = transitions
        self._places = places
        self._outputs = outputs

class PetriNetwork:
    def __init__(self,transitions=[], places=[], input_transitions=[], output_transitions=[]):
        self._transitions: list[Transitions] = transitions
        self._places: list[Places] = places
        self._inputs: list[Itransitions] = input_transitions
        self._outputs: list[Otransitions] = output_transitions

    def append_place(self, place: Places):
        self._places.append(place)

    def append_transition(self, transition: Transitions):
        self._transitions.append(transition)

    def append_t_input(self, place: Places, transition: Transitions, inputs: int):
        self._inputs.append(Itransitions(transition,place,inputs))

    def append_t_output(self, transition: Transitions, place: Places, outputs: int):
        self._outputs.append(Otransitions(transition,place,outputs))

    def print_inputs(self):
        set_inputs = set()
        dict_inputs = {}
        for param in self._inputs:
            set_inputs.add(param._transitions._transition)
        
        for p_set in set_inputs:
            dict_inputs[p_set] = []
            
        for param_set in set_inputs:
            for param_transition in self._inputs:
                if param_set == param_transition._transitions._transition:
                    dict_inputs[param_set].append(param_transition._places)
                
        for k,v in sorted(dict_inputs.items()):
            print(f'I({k}) =', end=" ")
            for val in v:
                print("{",val._pname,":",val._tokens,"}",  end=" ")
            print() 

    def print_outputs(self):
        set_outputs = set()
        dict_outputs = {}
        for param in self._outputs:
            set_outputs.add(param._transitions._transition)
        
        for p_set in set_outputs:
            dict_outputs[p_set] = []
            
        for param_set in set_outputs:
            for param_transition in self._outputs:
                if param_set == param_transition._transitions._transition:
                    dict_outputs[param_set].append(param_transition._places)
                
        for k,v in sorted(dict_outputs.items()):
            print(f'O({k}) =', end=" ")
            for val in v:
                print("{",val._pname,":",val._tokens,"}",  end=" ")
            print()    



    def show_network(self, param:str):
        print(param)
        print("C= (P,T,I,O)")
        print(f"P= {[place._pname for place in  self._places]}")
        print(f"T= {[transition._transition for transition in  self._transitions]}")
        # inputs
        print("\nInputs")
        self.print_inputs()
        
        # Outputs
        print("\nOutputs")
        self.print_outputs()
        print("-----------------------------------------------------")