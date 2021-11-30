from os import environ
import pandas as pd

class Environment:
    def __init__(self, environment_json):
        self.environment_json = environment_json

    def export_environment_variables(self):
        environment = {
            'all_entity_locations': [env['position'] for env in self.environment_json],
            'environment_json':self.environment_json
        }
        return environment
        
    