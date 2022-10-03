"""This class paint the graph about Petri Network"""
import graphviz
import random

def plot_graph():
  f = graphviz.Digraph('wide')
  f.attr(rankdir='LR', size='10,8')

  # transitions
  f.attr('node',shape='signature')
  for x in range(1,5):
    f.node(f't{x}',style='filled', fillcolor='#2ECC71')

  # places
  f.attr('node', shape='doublecircle')
  for x in range(1,6):
    f.node(name=f'P{x}',label=f'{random.randint(1,5)}',xlabel=f'P{x}')

  #inputs
  f.edge('P1','t1',label='<<font point-size="10">1</font>>')
  f.edge('P2','t2',label='<<font point-size="10">1</font>>')
  f.edge('P3','t2',label='<<font point-size="10">1</font>>')
  f.edge('P4','t2',label='<<font point-size="10">1</font>>')
  f.edge('P4','t3',label='<<font point-size="10">2</font>>')
  f.edge('P5','t4',label='<<font point-size="10">1</font>>')

  #outputs
  f.edge('t1','P4',label='<<font point-size="10">2</font>>')
  f.edge('t1','P3',label='<<font point-size="10">1</font>>')
  f.edge('t1','P2',label='<<font point-size="10">1</font>>')
  f.edge('t2','P2',label='<<font point-size="10">1</font>>')
  f.edge('t3','P5',label='<<font point-size="10">1</font>>')
  f.edge('t4','P4',label='<<font point-size="10">1</font>>')
  f.edge('t4','P3',label='<<font point-size="10">1</font>>')

  #title
  f.attr(label=r'\n\Transitions t1, t3, t4\nare enabled')
  return f
def plot_mat():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    fruits = ['apple', 'blueberry', 'cherry', 'orange']
    counts = [40, 100, 30, 55]
    bar_labels = ['red', 'blue', '_red', 'orange']
    bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('fruit supply')
    ax.set_title('Fruit supply by kind and color')
    ax.legend(title='Fruit color')

    plt.show()
if __name__=='__main__':
    # r = plot_graph()
    # r
    plot_mat()