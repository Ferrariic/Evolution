import math
import numpy as np

class Model:
    """
        Takes connection list, builds model, executes model for outputs
    """
    def __init__(self, brain, input_neurons, inner_neurons, output_neurons):
        self.brain = brain
        self.input_neurons = input_neurons
        self.inner_neurons = inner_neurons
        self.output_neurons = output_neurons
    
    def compile_and_run(self):
        try:
            if len(self.brain) == 0:
                '''brain could not be created.'''
                return {'brain_status':'No Thoughts Could Be Created'} 
            
            """
                Solve input layer
            """

            '''numpy conversion'''
            self.brain = np.asarray(self.brain)
            inputs = np.asarray([v for k,v in self.input_neurons.items()])
            hiddens = np.asarray([v for k,v in self.inner_neurons.items()])
            outputs = np.empty(len(self.output_neurons))

            '''input solve'''
            input_mask = self.brain[:,0] == 'input'
            output_mask = self.brain[input_mask][:,2] == 'output'
            hidden_mask = self.brain[input_mask][:,2] == 'inner'
            input_calculations = np.take(inputs, self.brain[input_mask][:,1].astype('uint8'))*self.brain[input_mask][:,4].astype(np.float) # calculate input layer to cast into inner and output

            '''assign inner and output values from input solve'''
            output_idx = self.brain[input_mask][output_mask][:,3].astype('uint8')
            outputs = np.bincount(output_idx, weights=input_calculations[output_mask].astype(np.float))

            hidden_idx = self.brain[input_mask][hidden_mask][:,3].astype('uint8')
            hiddens = np.bincount(hidden_idx, weights=input_calculations[hidden_mask].astype(np.float))

            """
                Solve Hidden Layer
            """

            '''builds masks'''
            hidden_solve_mask = self.brain[:,0] == 'inner'
            hidden_merge_mask = self.brain[hidden_solve_mask][:,2] == 'inner'
            output_final_mask = self.brain[hidden_solve_mask][:,2] == 'output'

            hiddens = np.tanh(hiddens) # Normalizes values
            '''solves hidden calculations'''
            
            if len(hiddens) == 0:
                if len(outputs)==0:
                    return {'brain_status':'No Thoughts Could Be Created'} 
                '''If there are no hidden values to solve for, just output outputs with tanh conversion'''
                choice = {'brain_status':str(np.argmax(np.tanh(outputs)))}
                return choice
            
            try:
                shift = np.max(self.brain[hidden_solve_mask][:,1].astype(np.uint8))-hiddens.shape[0]+1
                hiddens = np.pad(hiddens, (0, shift), 'constant')
            except ValueError:
                pass
            hidden_calculations = np.take(hiddens, self.brain[hidden_solve_mask][:,1].astype('uint8'))*self.brain[hidden_solve_mask][:,4].astype(np.float)

            '''hidden layer merges values'''
            hidden_merge_idx = self.brain[hidden_solve_mask][hidden_merge_mask][:,3].astype('uint8')
            hidden_temp = np.bincount(hidden_merge_idx, weights=hidden_calculations[hidden_merge_mask])
            if hidden_temp.shape == hiddens.shape:
                hiddens += hidden_temp
            hiddens = np.tanh(hiddens)

            """
                Solves output layer
            """
            '''output layer merges values'''
            output_temp_idx = self.brain[hidden_solve_mask][output_final_mask][:,3].astype('uint8')
            output_temp = np.bincount(output_temp_idx, weights=hidden_calculations[output_final_mask])

            '''finalizes'''
            if outputs.shape == output_temp.shape:
                outputs += output_temp
        
            if len(outputs)==0:
                # This error occurs when, for some reason, there is an inability to form a thought.
                return {'brain_status':'No Thoughts Could Be Created'}
            
            outputs = np.tanh(outputs)
            choice = {'brain_status':str(np.argmax(outputs))}
            return choice
        except Exception as e:
            #print(e)
            return {'brain_status':'No Thoughts Could Be Created'}