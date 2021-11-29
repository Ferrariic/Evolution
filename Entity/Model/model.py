import math

class Model:
    """
        Takes connection list, builds model, executes model for outputs
    """
    def __init__(self, connections, input_neurons, inner_neurons, output_neurons):
        self.connections = connections
        

    def __sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def compile_and_run(self):
        return