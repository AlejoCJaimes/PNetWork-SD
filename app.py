#   import modules
from Petri import *
from PetriEngine import *
from pprint import pprint


def load_data():
    petri = PetriNetwork()
    p1 = Places('p1', 1)
    p2 = Places('p2', 0)
    p3 = Places('p3', 0)
    p4 = Places('p4', 2)
    p5 = Places('p5', 1)

    t1 = Transitions('t1')
    t2 = Transitions('t2')
    t3 = Transitions('t3')
    t4 = Transitions('t4')

    petri.append_place(p1)
    petri.append_place(p2)
    petri.append_place(p3)
    petri.append_place(p4)
    petri.append_place(p5)

    petri.append_transition(t1)
    petri.append_transition(t2)
    petri.append_transition(t3)
    petri.append_transition(t4)

    petri.append_t_input(p1, t1, 1)
    petri.append_t_input(p2, t2, 1)
    petri.append_t_input(p3, t2, 1)
    petri.append_t_input(p4, t2, 1)
    petri.append_t_input(p4, t3, 2)
    petri.append_t_input(p5, t4, 1)

    petri.append_t_output(t1, p4, 2)
    petri.append_t_output(t1, p3, 1)
    petri.append_t_output(t1, p2, 1)
    petri.append_t_output(t2, p2, 1)
    petri.append_t_output(t3, p5, 1)
    petri.append_t_output(t4, p4, 1)
    petri.append_t_output(t4, p3, 1)
    return petri


if __name__ == '__main__':
    petri = load_data()
    pnet = PetriEngine(petri)
    pnet._pnet.show_network("Estructura Inicial 🚀")
    # shot t4
    pnet.next_transition("t4")
    pnet._pnet.show_network("Shoot t4! 🚀 ")
    # shot t1
    pnet.next_transition("t1")
    pnet._pnet.show_network("Shoot t1! 🚀 ")
    # shot t3
    pnet.next_transition("t3")
    pnet._pnet.show_network("Shoot t3! 🚀 ")

    