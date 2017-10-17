import copy
import itertools


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


water_system = State()
water_system = water_system.turn_on_tap()
water_system.display_state()
bread_first(water_system)
# states = infer(water_system)
# print()
# for s in states:
#     s.display_state()
#
# print()
# states = infer_list(states)
# for s in states:
#     s.display_state()
# #
# states = infer_list(states)
# print()
# for s in states:
#     s.display_state()
#
# states = infer_list(states)
# print()
# for s in states:
#     s.display_state()
#
# states = infer_list(states)
# print()
# for s in states:
#     s.display_state()
