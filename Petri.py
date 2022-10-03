""" Petri library, contains all class about the Petri network
Transitions, Places, Inputs(t) and Outputs(t)"""
import numpy as np
import json
import os 
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
        self._transitions: np.array([Transitions]) = transitions
        self._places: np.array([Places]) = places
        self._inputs: np.array([Itransitions]) = input_transitions
        self._outputs: np.array([Otransitions]) = output_transitions

    def append_place(self, place: Places):
        self._places = np.append(self._places,place)
        # self._places.append(place)

    def append_transition(self, transition: Transitions):
        self._transitions = np.append(self._transitions,transition)
        # self._transitions.append(transition)

    def append_t_input(self, place: Places, transition: Transitions, inputs: int):
        self._inputs = np.append(self._inputs,Itransitions(transition,place,inputs))
        # self._inputs.append(Itransitions(transition,place,inputs))

    def append_t_output(self, transition: Transitions, place: Places, outputs: int):
        self._outputs = np.append(self._outputs, Otransitions(transition,place,outputs))
        # self._outputs.append(Otransitions(transition,place,outputs))

    def get_arc_inputs(self, tname:str):
        arc = [(a._places._pname,a._inputs) for a in self._inputs if a._transitions._transition == tname]
        return arc
    def get_arc_outputs(self, tname:str):
        arc = [(a._places._pname,a._outputs) for a in self._outputs if a._transitions._transition == tname]
        return arc
    
    def get_places(self,):
        return [p for p in self._places] 
    
    def get_marks(self,):
        marks = self.get_places()
        return [m._tokens for m in marks]
    
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
    
    def json_load(self, filename:str):
        """ Load json file in form of petri networks"""
        # opening json
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir,f'./json/load/{filename}.json')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name)
        
        # return json object
        data = json.load(f)
        
        # handling network
        t_places = []
        t_transitions = []
        inputs = []
        outputs = []
        
        # add places
        places = dict(zip(data['places']['names'], 
                        data['places']['tokens']
                        ))
        for place,token in places.items():
            t_places.append(Places(place,token))

        
        # add transitions
        transitions = data['transitions']
        for t_name in transitions:
            t_transitions.append(Transitions(t_name))

        # add inputs
        n_inputs = len(data['inputs']['places']['tokens'])
        # print(n_inputs)
        for i in range(n_inputs):
            # temporal variables
            tmp_transition = data['inputs']['transitions'][i]
            tmp_places = data['inputs']['places']['pname'][i]
            tmp_tokens = data['inputs']['places']['tokens'][i]
            tmp_arc = data['inputs']['arc'][i]
            # append inputs
            inputs.append(Itransitions(Transitions(tmp_transition),Places(tmp_places,tmp_tokens),inputs=tmp_arc))

        
        # add outputs
        n_outputs = len(data['outputs']['places']['tokens'])
        # print(n_inputs)
        for i in range(n_outputs):
            # temporal variables
            tmp_transition = data['outputs']['transitions'][i]
            tmp_places = data['outputs']['places']['pname'][i]
            tmp_tokens = data['outputs']['places']['tokens'][i]
            tmp_arc = data['outputs']['arc'][i]
            # append inputs
            outputs.append(Otransitions(Transitions(tmp_transition),Places(tmp_places,tmp_tokens),outputs=tmp_arc))
        return PetriNetwork(t_transitions,t_places,inputs,outputs)
    
    def json_export(self, filename:str):
        """ Export json with indent=3ptos """      
        json_dic = {}
        json_dic = {
        "places" : {"names": [p._pname for p in self._places], 
                    "tokens": [p._tokens for p in self._places]
                   },
        "transitions" : [t._transition for t in self._transitions],
        "inputs" : {
                     "places" : {
                                "pname" :  [input._places._pname for input in self._inputs],
                                "tokens":  [input._places._tokens for input in self._inputs]
                                }
                        ,
                     "transitions": [input._transitions._transition for input in self._inputs],
                     "arc" :[input._inputs for input in self._inputs]
                   },
        "outputs" : {
                     "places" : {
                                "pname" :  [output._places._pname for output in self._outputs],
                                "tokens":  [output._places._tokens for output in self._outputs]
                                }
                        ,
                     "transitions": [output._transitions._transition for output in self._outputs],
                     "arc" :[output._outputs for output in self._outputs]
                   },
        }
        # Serializing json  
        json_object = json.dumps(json_dic, indent = 3) 
        
        # export in route
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir,f'./json/export/{filename}+_shot.json')
        file_name = os.path.abspath(os.path.realpath(file_name))
        
        # saving json
        with open(file_name,'w') as outfile:
            outfile.write(json_object)
        