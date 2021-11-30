import math

class Model:
    """
        Takes connection list, builds model, executes model for outputs
    """
    def __init__(self, brain, input_neurons, inner_neurons, output_neurons):
        self.brain = brain
        self.input_neurons = input_neurons
        self.inner_neurons = inner_neurons
        self.output_neurons = output_neurons
        
    def __sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def compile_and_run(self):
        # Solve hidden layers first
        hidden_neuron_computation = dict()
        for connection in self.brain:
            if connection[2] == 'inner':
                from_type = connection[0]
                from_id = connection[1]
                inner_id = connection[3]
                weight = connection[4]

                if from_type == 'inner':
                    try:
                        hidden_neuron_computation[str(inner_id)] = (self.inner_neurons[str(from_id)]*weight)+hidden_neuron_computation[str(inner_id)]
                    except:
                        try:
                            hidden_neuron_computation[str(inner_id)] = dict()
                            hidden_neuron_computation[str(inner_id)] = (self.inner_neurons[str(from_id)]*weight)
                        except:
                            pass

                if from_type == 'input':
                    try:
                        hidden_neuron_computation[str(inner_id)] = (self.input_neurons[str(from_id)]*weight)+hidden_neuron_computation[str(inner_id)]
                    except:
                        try:
                            hidden_neuron_computation[str(inner_id)] = dict()
                            hidden_neuron_computation[str(inner_id)] = (self.input_neurons[str(from_id)]*weight)
                        except:
                            pass

        hidden_neuron_values = dict()
        for key, value in hidden_neuron_computation.items():
            try:
                hidden_neuron_values[key] = self.__sigmoid(value)
            except:
                pass
        
        # Solve output layers
        output_neuron_computation = dict()
        for connection in self.brain:
            if connection[2] == 'output':

                from_type = connection[0]
                from_id = connection[1]
                outer_id = connection[3]
                weight = connection[4]
                
                if from_type == 'inner':
                    try:
                        output_neuron_computation[str(outer_id)] = (hidden_neuron_values[str(from_id)]*weight)+output_neuron_computation[str(outer_id)]
                    except:
                        try:
                            output_neuron_computation[str(outer_id)] = dict()
                            output_neuron_computation[str(outer_id)] = (hidden_neuron_values[str(from_id)]*weight)
                        except:
                            pass
                            
                if from_type == 'input':
                    try:
                        output_neuron_computation[str(outer_id)] = (self.input_neurons[str(from_id)]*weight)+output_neuron_computation[str(outer_id)]
                    except:
                        try:
                            output_neuron_computation[str(outer_id)] = dict()
                            output_neuron_computation[str(outer_id)] = (self.input_neurons[str(from_id)]*weight)
                        except:
                            pass
                        
        output_values = dict()
        for key, value in output_neuron_computation.items():
            try:
                output_values[key] = self.__sigmoid(value)
            except:
                pass

        try:
            best_choice = max(output_values, key=output_values.get)
        except:
            return {'brain_status':'ERROR'}
        return {'brain_status':best_choice}