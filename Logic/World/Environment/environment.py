from os import environ
import pandas as pd
import json
            
class Environment:
    def __init__(self, environment_json):
        self.environment_json = environment_json

    def export_environment_variables(self):
        environment = {
            'all_entity_locations': [env['position'] for env in self.environment_json],
            'all_entity_colors': [env['color'] for env in self.environment_json],
            'all_entity_names':[env['name'] for env in self.environment_json],
            'environment_json':self.environment_json
        }
        
        with open("Logic/World/Data/data.json", 'w') as f:
            json.dump(environment, f)
        return environment
        
    