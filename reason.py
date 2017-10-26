import copy
import itertools
from graphviz import Digraph


class Quantity:
    """
    class to represent a quantity in a qualitive model.
    """

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


class State:

    def display_state(self):
        """
        display the state to stdout
        """
        print('-----------')
        for name, quantity in self.quantities.items():
            print(name, quantity.quantity, quantity.derivative)

    def turn_on_tap(self):
        """
        exogenoeus event to turn on tap sets derivative of the inflow to
        positve
        """
        copy = self.copy()
        copy.quantities['inflow'].set_derivative_positive()
        return copy

    def copy(self):
        return copy.deepcopy(self)

    def __init__(self):
        outflow = Quantity(['0', '+', 'max'])
        volume = Quantity(['0', '+', 'max'])
        inflow = Quantity(['0', '+'])
        height = Quantity(['0', '+', 'max'])
        pressure = Quantity(['0', '+', 'max'])

        self.quantities = {
            'outflow': outflow, 'volume': volume, 'inflow': inflow,
            'pressure': pressure, 'height': height
        }


def proportional(state, a, b):
    """
    p plus relationship between a and b in state.
    """
    if state.quantities[a].derivative == '+':
        if state.quantities[b].derivative == '-':
            state.quantities[b].derivative = '0'
        if state.quantities[b].derivative == '0':
            state.quantities[b].derivative = '+'
    if state.quantities[a].derivative == '-':
        if state.quantities[b].derivative == '+':
            state.quantities[b].derivative = '0'
        if state.quantities[b].derivative == '0':
            state.quantities[b].derivative = '-'
    return state


def vc(state, a, b):
    """
    vc max and vc zero between a and b in state.
    """
    if state.quantities[a].quantity == 'max':
        state.quantities[b].quantity = 'max'
    if state.quantities[a].quantity == '0':
        state.quantities[b].quantity = '0'
    return state


def iPplusMinus(state, a, b, c):
    """
    i plus and i minus relationship between a, b and c.
    """
    q1 = state.quantities[a]
    q2 = state.quantities[b]

    if q1.quantity == '0' and q2.quantity == '0':
        return [state]

    if q1.quantity == '0' and (q2.quantity == '+' or q2.quantity == 'max'):
        if state.quantities[c].derivative == '0':
            state.quantities[c].derivative = '-'
        if state.quantities[c].derivative == '+':
            state.quantities[c].derivative = '0'
        return [state]

    if q1.quantity == '+' and q2.quantity == '0':
        if state.quantities[c].derivative == '0':
            state.quantities[c].derivative = '+'
        if state.quantities[c].derivative == '-':
            state.quantities[c].derivative = '0'
        return [state]

    if q1.quantity == '+' and (q2.quantity == '+' or q2.quantity == 'max'):
        if state.quantities[c].derivative == '-':
            copy1 = state.copy()
            copy1.quantities[c].derivative = '0'
            return [copy1, state]
        if state.quantities[c].derivative == '0':
            copy1 = state.copy()
            copy2 = state.copy()
            copy1.quantities[c].derivative = '0'
            copy2.quantities[c].derivative = '+'
            return [copy1, copy2, state]
        if state.quantities[c].derivative == '+':
            copy1 = state.copy()
            copy1.quantities[c].derivative = '0'
            return [state, copy1]


def derivative(state):
    """
    apply derivative to the quantities in state.
    """
    copy = state.copy()
    for name, q in state.quantities.items():
        index = q.space.index(q.quantity)
        if q.derivative == '+' and (index + 1) != len(q.space):
            copy.quantities[name].quantity = q.space[index + 1]
        if q.derivative == '-' and (index) != 0:
            copy.quantities[name].quantity = q.space[index - 1]
    return copy


def derivative2(state):
    """
    makes sure maximum can't have positive derivative and 0 can't have
    negative derivative.
    """
    copy = state.copy()
    for name, q in state.quantities.items():
        if copy.quantities[name].quantity == 'max' and copy.quantities[name].derivative == '+':
            copy.quantities[name].derivative = '0'
        if copy.quantities[name].quantity == '0' and copy.quantities[name].derivative == '-':
            copy.quantities[name].derivative = '0'
    return copy


def polynomial_tap(state):
    """
    models polynomial curve of the tap.
    """
    copy = state.copy()
    if state.quantities['inflow'].derivative == '+':
        copy.quantities['inflow'].derivative = '0'
        return [copy, state]
    if state.quantities['inflow'].derivative == '0':
        copy.quantities['inflow'].derivative = '-'
        return [copy, state]
    return [state]


def infer(state):
    """
    does one inference step on state.
    """
    der_app_state = derivative(state)
    der_app_state = vc(der_app_state, 'volume', 'height')
    der_app_state = vc(der_app_state, 'volume', 'outflow')
    der_app_state = vc(der_app_state, 'height', 'volume')
    der_app_state = vc(der_app_state, 'height', 'pressure')
    der_app_state = vc(der_app_state, 'pressure', 'height')
    der_app_state = vc(der_app_state, 'pressure', 'outflow')
    next_states = iPplusMinus(der_app_state, 'inflow', 'outflow', 'volume')
    next_states = [proportional(s, 'volume', 'height') for s in next_states]
    next_states = [proportional(s, 'height', 'pressure') for s in next_states]
    next_states = [proportional(s, 'pressure', 'outflow') for s in next_states]
    next_states = list(itertools.chain(*[polynomial_tap(s) for s in next_states]))
    next_states = [derivative2(s) for s in next_states]
    return next_states


def infer_list(states):
    return list(itertools.chain(*[infer(s) for s in states]))


def mappi(state):
    return tuple([(state.quantities[s].quantity, state.quantities[s].derivative)
                 for s in state.quantities])


class Tree:
    """
    tree to represent stategraph.
    """

    def bread(self):
        """
        bread first search trough the search tree to get al the states.
        """
        to_do = self.leaf_nodes
        visited = {mappi(to_do[0]['state']): {'number': to_do[0]['number'],
                                              'children': []}}
        while to_do:
            node = to_do.pop()
            next_states = infer(node['state'])
            node['children'] = []
            for state in next_states:
                visited_already = visited.get(mappi(state))
                if not visited_already:
                    self.amount_of_nodes += 1
                    new_node = {'state': state, 'number': self.amount_of_nodes}
                    visited[mappi(state)] = {'number': self.amount_of_nodes,
                                             'children': []}
                    to_do.append(new_node)
                visited.get(mappi(node['state']))['children'].append(mappi(state))
                node['children'].append(new_node)
        return visited

    def __init__(self, root):
        self.amount_of_nodes = 1
        self.root = {'state': root, 'number': 1}
        self.leaf_nodes = [self.root]


def state_to_string(state):
    """
    maps a state to a string representation.
    """
    return ('i: \t' + str(state[2][0]) + '\t' + str(state[2][1]) + '\n'
            'v: \t' + str(state[1][0]) + '\t'+str(state[1][1]) + '\n'
            'o: \t' + str(state[0][0]) + '\t'+str(state[0][1]) + '\n'
            'h: \t' + str(state[3][0]) + '\t'+str(state[3][1]) + '\n'
            'p: \t' + str(state[4][0]) + '\t'+str(state[4][1]) + '\n')


dot = Digraph(comment='State  Graph.')
water_system = State()
dot.node('0', state_to_string(mappi(water_system)))
dot.edge('0', '1')
water_system = water_system.turn_on_tap()

t = Tree(water_system)
result = t.bread()

edges = set()
for key, value in result.items():
    number = value['number']
    dot.node(str(number), state_to_string(key))
    for child in value['children']:
        edge = str(number) + str(result[child]['number'])
        if edge not in edges and number != result[child]['number']:
            dot.edge(str(number), str(result[child]['number']))
        edges.add(edge)

dot.render('test-output/state-graph.gv', view=True)
