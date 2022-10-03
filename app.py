#   import modules
from Petri import *
from PetriEngine import *
    

if __name__ == '__main__':
    petri = PetriNetwork().json_load('petri_network')
    pnet = PetriEngine(petri)
    pnet._pnet.show_network("Estructura Inicial 🚀")
    pnet.check_enable_transitions()
    # # shot t4
    pnet.next_transition("t4")
    pnet._pnet.show_network("Shoot t4! 🚀 ")
    # # # shot t1
    # pnet.next_transition("t1")
    # pnet._pnet.show_network("Shoot t1! 🚀 ")
    # # # shot t3
    # pnet.next_transition("t3")
    # pnet._pnet.show_network("Shoot t3! 🚀 ")
    

    