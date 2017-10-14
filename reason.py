class Quantity:

    quantity = '0'
    derivative = '0'

    def set_derivative_positive(self):
        self.derivative = '+'

    def __init__(self, space):
        self.space = space


class State:

    def turn_on_tap(self):
        self.quantities['inflow'].set_derivative_positive()

    def display_state(self):
        for name, quantity in self.quantities.items():
            print(name, quantity.quantity, quantity.derivative)

    def __init__(self):

        outflow = Quantity(['0', '+'])
        volume = Quantity(['0', '+', 'max'])
        inflow = Quantity(['0', '+', 'max'])

        self.quantities = {
            'outflow': outflow, 'volume': volume, 'inflow': inflow
        }

        self.dependencies = {
            (inflow, volume, 'i+'),
            (outflow, inflow, 'i-'),
            (volume, outflow, 'p+'),
            (outflow, volume, 'vc_max'),
            (volume, outflow, 'vc_0')
        }


initial_state = State()
initial_state.display_state()
