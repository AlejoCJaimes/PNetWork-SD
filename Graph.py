"""This class paint the graph about Petri Network"""
import graphviz
from Petri import *
from PetriEngine import *

class Graphic:
  def __init__(self,petri:PetriNetwork):
    self._petri = petri 
    self._pnet = PetriEngine(petri)
    
  def plot_graph(self,_name='wide',_rankdir='LR',
                 _size='10,8',_shapet='signature',_shapep='doublecircle'):
    # initial parameters
    f = graphviz.Digraph(name=_name)
    f.attr(rankdir=_rankdir, size=_size)
    
    # Create transitions
    f.attr('node',shape=_shapet)
    for t in self._petri._transitions:
      if self._pnet.check_state_transition(t._transition):
        f.node(t._transition,style='filled', fillcolor='#2ECC71')
      else:
        f.node(t._transition,style='filled', fillcolor='#E74C3C')
    t_enable = f'\n\Transitions{self._pnet.check_enable_transitions()}\nare enabled'
    
    # Create places
    f.attr('node', shape=_shapep)
    for p in self._petri._places:
      f.node(name=p._pname,label=str(p._tokens),xlabel=p._pname)
    
    # Create inputs
    for input in self._petri._inputs:
      p=input._places._pname
      t=input._transitions._transition
      i=input._inputs
      f.edge(p,t,label=f'<<font point-size="10">{i}</font>>')
    
    # Create outputs      
    for output in self._petri._outputs:
      p=output._places._pname
      t=output._transitions._transition
      o=output._outputs
      f.edge(t,p,label=f'<<font point-size="10">{o}</font>>')
      
    f.attr(label=rf'{t_enable}')  
    return f
    
    