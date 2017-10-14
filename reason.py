class Quantity:

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


def iPlus(a, b):
    if a.derivative == '+':
        b.derivative = '+'


def iMinus(a, b):
    if a.derivative == '+':
        b.derivative = '-'


def vcMax(a, b):
    if a.quantity == 'max':
        b.quantity = 'max'


def vcZeros(a, b):
    if a.quantity == '0':
        b.quantity = 0


class State:

    def turn_on_tap(self):
        self.quantities['inflow'].set_derivative_positive()

    def display_state(self):
        print('-----------')
        for name, quantity in self.quantities.items():
            print(name, quantity.quantity, quantity.derivative)

    def infer(self):
        for f in self.dependencies:
            f()

    def __init__(self):

        outflow = Quantity(['0', '+'])
        volume = Quantity(['0', '+', 'max'])
        inflow = Quantity(['0', '+', 'max'])

        self.quantities = {
            'outflow': outflow, 'volume': volume, 'inflow': inflow
        }

        self.dependencies = [
            lambda: iPlus(inflow, volume),
            lambda: iMinus(outflow, volume),
            lambda: vcMax(volume, outflow),
            lambda: vcZeros(volume, outflow)
        ]


state = State()
state.display_state()
state.turn_on_tap()
state.display_state()
state.infer()
state.display_state()
