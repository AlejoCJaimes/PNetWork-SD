from socket import TCP_INFO
from Petri import *

class PetriEngine:
    def __init__(self, pnet: PetriNetwork) -> None:
        self._pnet = pnet
    
    def get_e_j(self,t_function: list, places:list):
        return np.array([self.get_arc_by_place(t_function,p._pname) for p in places],dtype=int)
    
    def check_state_transition(self,t_name:str):
        ''' 
        validate if n_token according on the place is greater than or equal to n_inputs (arcs)
        '''
        trans = [x._transition for x in self._pnet._transitions if x._transition == t_name]
        if trans == []:
            return False
        else:    
            places = self._pnet.get_places()
            t_inputs = self._pnet.get_arc_inputs(t_name)
            
            # check if u >= e[j]
            e_j = self.get_e_j(t_inputs,places)
            u = np.array([p._tokens for p in places],dtype=int)
            
            return np.all(u >= e_j)
    
    def update_tokens(self, new_mark:np):
            m = 0
            for place in self._pnet._places:
                place._tokens = new_mark[m]
                m = m+1
    
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
    def get_dmatrix_min(self):
        """ Generate and returns 
        the D- Matrix (input functions)
        """
        
        # get transitions and places
        trans = [x._transition for x in self._pnet._transitions]
        places = [p._pname for p in self._pnet._places]
        arg = []
        
        # iterate overt transitions and get the arc by places
        for t in trans:
            inps = self._pnet.get_arc_inputs(t)
            for p in places:
                arcs = self.get_arc_by_place(inps,p)
                arg.append(arcs)        
        
        # tam matrix
        t  = len(trans)
        p = len(places)
        
        # return D- matrix
        d_m = np.array(arg,dtype=int)
        d_m = np.reshape(d_m,(t,p))
        return d_m
        
    def get_dmatrix_plus(self):
        """ Generate and returns 
        the D+ Matrix (output functions)
        """
        
        # get transitions and places
        trans = [x._transition for x in self._pnet._transitions]
        places = [p._pname for p in self._pnet._places]
        arg = []
        
        # iterate overt transitions and get the arc by places
        for t in trans:
            inps = self._pnet.get_arc_outputs(t)
            for p in places:
                arcs = self.get_arc_by_place(inps,p)
                arg.append(arcs)        
        
        # tam matrix
        t  = len(trans)
        p = len(places)
        
        # return D- matrix
        d_p = np.array(arg,dtype=int)
        d_p = np.reshape(d_p,(t,p))
        return d_p

    def check_enable_transitions(self):
        transitions = self._pnet._transitions
        available = np.array([t._transition for t in transitions if self.check_state_transition(t._transition)])
        return available
    
    def next_transition(self, t_name: str):
        self.shoot_transition(t_name)
        
    def shoot_transition(self,t_name:str):
        is_valid = self.check_state_transition(t_name)

        output = ""
        if is_valid:
            
            marks,t_inputs,t_outputs = self.get_elements_to_shoot(t_name=t_name)
            # fire 
            new_mark = np.array(marks -  t_inputs + t_outputs)
            self.update_tokens(new_mark)
    
            # update transitions
            self.update_transitions()
            
            # save transition
            self._pnet.json_export(t_name)
            
            output = f"Fired --> {t_name}"
        else:
            self.print_err(t_name)
        return output    
            
    def get_arc_by_place(self,tp_transition:list,place:str):
        for x in range(len(tp_transition)):
            if tp_transition[x][0] == place:
                return tp_transition[x][1]
        return 0
    
    def get_elements_to_shoot(self,t_name:str):
        places = self._pnet.get_places()
        t_inputs = self._pnet.get_arc_inputs(t_name)
        t_outputs = self._pnet.get_arc_outputs(t_name)
        e_t_inputs = np.array(self.get_e_j(t_inputs,places))
        e_t_outputs = np.array(self.get_e_j(t_outputs,places))
        marks = np.array(self._pnet.get_marks())
        return marks,e_t_inputs,e_t_outputs
    
    def print_err(self,t_name:str):
        print(f"Lo sentimos 🚩.\nTransición {t_name} no está habilitada.")
        print("Detalles:\n")
        t_inputs_err = [t for t in self._pnet._inputs if t._transitions._transition == t_name]
        for transition in t_inputs_err:
            print(f"Tokens: {transition._places._tokens} Inputs: {transition._inputs}")