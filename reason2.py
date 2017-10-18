import copy
import itertools
from graphviz import Digraph

class Quantity:

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


class State:

    def display_state(self):
        print('-----------')
        for name, quantity in self.quantities.items():
            print(name, quantity.quantity, quantity.derivative)

    def turn_on_tap(self):
        copy = self.copy()
        copy.quantities['inflow'].set_derivative_positive()
        return copy

    def copy(self):
        return copy.deepcopy(self)

    def __init__(self):
        outflow = Quantity(['0', '+', 'max'])
        volume = Quantity(['0', '+', 'max'])
        inflow = Quantity(['0', '+'])

        self.quantities = {
            'outflow': outflow, 'volume': volume, 'inflow': inflow
        }

def proportional(state, a, b):
    if state.quantities[a].derivative == '+' and state.quantities[b].quantity != '+':
        state.quantities[b].derivative = '+'
    return state

def vc(state, a, b):
    if state.quantities[a].quantity == 'max':
        state.quantities[b].quantity = 'max'
    if state.quantities[a].quantity == '0':
        state.quantities[b].quantity = '0'
    return state

def iPplusMinus(state, a, b, c):
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
    copy = state.copy()
    for name, q in state.quantities.items():
        index = q.space.index(q.quantity)
        if q.derivative == '+' and (index + 1) != len(q.space):
            copy.quantities[name].quantity = q.space[index + 1]
        if q.derivative == '-' and (index) != 0:
            copy.quantities[name].quantity = q.space[index - 1]

        if copy.quantities[name].quantity == 'max' and copy.quantities[name].derivative == '+':
            copy.quantities[name].derivative = '0'
        if copy.quantities[name].quantity == '0' and copy.quantities[name].derivative == '-':
            copy.quantities[name].derivative = '0'

    return copy


def polynomial_tap(state):
    copy = state.copy()
    if state.quantities['inflow'].derivative == '+':
        copy.quantities['inflow'].derivative = '0'
        return [copy, state]
    if state.quantities['inflow'].derivative == '0':
        copy.quantities['inflow'].derivative = '-'
        return [copy, state]
    return [state]


def infer(state):
    der_app_state = derivative(state)
    der_app_state = vc(der_app_state, 'volume', 'outflow')
    next_states = iPplusMinus(der_app_state, 'inflow', 'outflow', 'volume')
    next_states = [proportional(s, 'volume', 'outflow') for s in next_states]
    # next_states = [vc(s, 'volume', 'outflow') for s in next_states]
    next_states = list(itertools.chain(*[polynomial_tap(s) for s in next_states]))
    return next_states


def infer_list(states):
    return list(itertools.chain(*[infer(s) for s in states]))


def mappi(state):
    return tuple([(state.quantities[s].quantity, state.quantities[s].derivative)
                 for s in state.quantities])


class Tree:

    def bread_first(state):
        visited = {mappi(state)}
        states = infer_list([state])
        print('********')
        for s in states:
            s.display_state()
        while states:
            print('********')
            states = [x for x in infer_list(states) if mappi(x) not in visited]
            for s in states:
                s.display_state()
            for s in states:
                visited.add(mappi(s))
        print('bgbgbgb', len(visited))

    def bread(self):
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
                    visited[mappi(state)] = {'number': self.amount_of_nodes, 'children': []}
                    to_do.append(new_node)
                visited.get(mappi(node['state']))['children'].append(mappi(state))
                node['children'].append(new_node)
        return visited

    def __init__(self, root):
        self.amount_of_nodes = 1
        self.root = {'state': root, 'number': 1}
        self.leaf_nodes = [self.root]


water_system = State()
water_system = water_system.turn_on_tap()

t = Tree(water_system)
result = t.bread()

dot = Digraph(comment='The Round Table')


def state_to_string(state):
    return 'i: ' + str(state[2][0])+str(state[2][1]) + 'v: ' + str(state[1][0])+str(state[1][1]) + 'o: ' + str(state[0][0])+str(state[0][1])


for key, value in result.items():
    number = value['number']
    dot.node(str(number), state_to_string(key))
    for child in value['children']:
        dot.edge(str(number), str(result[child]['number']))

# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
dot.render('test-output/round-table.gv', view=True)
