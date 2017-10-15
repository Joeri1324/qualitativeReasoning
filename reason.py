import copy


class Quantity:

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


def iPlus(state, a, b):
    copy = state.copy()
    if state.quantities[a].derivative == '+':
        copy.quantities[b].derivative = '+'
        return copy
    return False


def iMinus(state, a, b):
    copy = state.copy()
    if state.quantities[a].derivative == '+':
        copy.quantities[b].derivative = '-'
        return copy
    return False


def vcMax(state, a, b):
    copy = state.copy()
    if state.quantities[a].quantity == 'max' and state.quantities[b].quantity != 'max':
        copy.quantities[b].quantity = 'max'
        return copy
    return False


def vcZeros(state, a, b):
    copy = state.copy()
    if state.quantities[a].quantity == '0' and state.quantities[b].quantity != '0':
        copy.quantities[b].quantity = 0
        return copy
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
        return [f[0](self, f[1], f[2]) for f in self.dependencies
                if f[0](self, f[1], f[2])]

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
            (vcZeros, 'volume', 'outflow')
        ]


state = State()
state.display_state()
new_state = state.turn_on_tap()
new_state.display_state()

for s in new_state.infer():
    s.display_state()
