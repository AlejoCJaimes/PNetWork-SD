from Petri import *

class PetriEngine:
    def __init__(self, pnet: PetriNetwork) -> None:
        self._pnet = pnet

    def get_inputs_t(self, t_name: str):
        '''
        return all inputs where t_name 'll equals to name of transitions of input
        '''
        t_inputs = [t for t in self._pnet._inputs if t._transitions._transition == t_name]
        return t_inputs
    
    def get_outputs_t(self, t_name: str):
        '''
        return all inputs where t_name 'll equals to name of transitions of output
        '''
        t_outputs = [t for t in self._pnet._outputs if t._transitions._transition == t_name]
        return t_outputs

    def check_state_transition(self, t_name : str):
        ''' 
        validate if n_token according on the place is greater than or equal to n_inputs (arcs)
        '''
        t_inputs = self.get_inputs_t(t_name)
        is_valid = True
        for transition in t_inputs:
            if not transition._places._tokens >= transition._inputs:
                is_valid = False
        return is_valid

    def update_transitions(self):
        # input transition
            for transition in self._pnet._inputs:
                for place in self._pnet._places:
                    if transition._places._pname == place._pname:
                        transition._places._tokens = place._tokens
        # output transition
            for transition in self._pnet._outputs:
                for place in self._pnet._places:
                    if transition._places._pname == place._pname:
                        transition._places._tokens = place._tokens
        
    def print_err(self,t_name:str):
        print(f"Lo sentimos 🚩.\nTransición {t_name} no está habilitada.")
        print("Detalles:\n")
        t_inputs_err = self.get_inputs_t(t_name)
        for transition in t_inputs_err:
            print(f"Place: {transition._places._pname} Tokens: {transition._places._tokens} Inputs: {transition._inputs}")


    def shoot_transition(self,t_name:str):
        is_valid = self.check_state_transition(t_name)

        output = ""
        if is_valid:
            # related transitions
            t_inputs = self.get_inputs_t(t_name)
            t_outputs = self.get_outputs_t(t_name)
            
            # fire
            # input transition
            for transition in t_inputs:
                for place in self._pnet._places:
                    if transition._places._pname == place._pname:
                        # new_state = current_state - t_input + t_output
                        place._tokens -= transition._inputs
            # output transition
            for transition in t_outputs:
                for place in self._pnet._places:
                    if transition._places._pname == place._pname:
                        # new_state = current_state - t_input + t_output
                        place._tokens += transition._outputs
            
            # update transitions
            self.update_transitions()
            output = f"Fired --> {t_name}"
        else:
            self.print_err(t_name)
        return output

    def next_transition(self, t_name: str):
        self.shoot_transition(t_name)