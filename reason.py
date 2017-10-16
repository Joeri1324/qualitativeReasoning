import copy


class Quantity:

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


def iPlus(state, a, b):
    if state.quantities[a].quantity == '+':
        state.quantities[b].derivative = '+'
    return state


def iMinus(state, a, b):
    if state.quantities[a].quantity == '+':
        state.quantities[b].derivative = '-'
    return state


def vcMax(state, a, b):
    if state.quantities[a].quantity == 'max' and state.quantities[b].quantity != 'max':
        state.quantities[b].quantity = 'max'
    return state


def vcZeros(state, a, b):
    if state.quantities[a].quantity == '0' and state.quantities[b].quantity != '0':
        state.quantities[b].quantity = '0'
    return state


def proportional(state, a, b):
    if state.quantities[a].derivative == '+' and state.quantities[b].quantity != '+':
        state.quantities[b].derivative = '+'
    return state


def derivative(state, quantities, _):
    mutation = False
    for q in quantities:
        index = state.quantities[q].space.index(state.quantities[q].quantity)
        if state.quantities[q].derivative == '+' and (index + 1) != len(state.quantities[q].space):
            state.quantities[q].quantity = state.quantities[q].space[index + 1]
            mutation = True
        if state.quantities[q].derivative == '-' and (index ) != 0:
            state.quantities[q].quantity = state.quantities[q].space[index - 1]
            mutation = True
    if mutation:
        return state
    return False


class State:

    def turn_on_tap(self):
        copy = self.copy()
        copy.quantities['inflow'].set_derivative_positive()
        return copy

    def display_state(self):
        print('-----------')
        for name, quantity in self.quantities.items():
            print(name, quantity.quantity, quantity.derivative)

    def infer(self):
        copy = self.copy()
        result = derivative(copy, ['inflow', 'outflow', 'volume'], 'hoi')
        if result:
            return result
        for f in self.dependencies:
            copy = f[0](copy, f[1], f[2])
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

        self.dependencies = [
            (iPlus, 'inflow', 'volume'),
            (iMinus, 'outflow', 'volume'),
            (vcMax, 'volume', 'outflow'),
            (vcZeros, 'volume', 'outflow'),
            (proportional, 'volume', 'outflow'),
        ]


state = State()
state.display_state()
new_state = state.turn_on_tap()
new_state.display_state()

ss = new_state.infer()
ss.display_state()
ss = ss.infer()
ss.display_state()
ss = ss.infer()
ss.display_state()
ss = ss.infer()
ss.display_state()
ss = ss.infer()
ss.display_state()
