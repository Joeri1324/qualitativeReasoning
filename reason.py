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
        index = state.quantities[b].space.index(state.quantities[b].quantity)
        state.quantities[b].derivative = state.quantities[b].space[index-1]
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

def iPplusMinus(state, fish, _):
    copy = state.copy()
    [a, b, c] = fish
    q1 = state.quantities[a]
    q2 = state.quantities[b]
    if (q1.quantity == '-' and q2.quantity == '-') or (q1.quantity == '-' and 
        q1.quantity == '0') or (q1.quantity == '0' and q1.quantity == '-'):
        state.quantities[c].derivative = '-' # shift 
        return state
    if (q1.quantity == '+' and q2.quantity == '+') or (q1.quantity == '+' and 
        q1.quantity == '0') or (q1.quantity == '0' and q1.quantity == '+'):    
        state.quantities[c].derivative = '+' # shift
    if (q1.quantity == '0' and q2.quantity == '0'):
        return state
    if (q1.quantity == '+' and q1.quantity == '-') or (q1.quantity == '-' and q1.quantity == '+'):
        copy.quantities[c]



def derivative(state, quantities, _):
    copy = state.copy()
    mutation = False
    for q in quantities:
        index = state.quantities[q].space.index(state.quantities[q].quantity)
        if state.quantities[q].derivative == '+' and (index + 1) != len(state.quantities[q].space):
            copy.quantities[q].quantity = state.quantities[q].space[index + 1]
            mutation = True
        if state.quantities[q].derivative == '-' and (index ) != 0:
            copy.quantities[q].quantity = state.quantities[q].space[index - 1]
            mutation = True
    return copy



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
            (derivative, ['inflow', 'outflow', 'volume'], 'hoi'),
            (vcMax, 'volume', 'outflow'),
            (vcZeros, 'volume', 'outflow'),
            (proportional, 'volume', 'outflow'),
            (iPplusMinus, ['inflow', 'outflow', 'volume'], 'hoi')
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
