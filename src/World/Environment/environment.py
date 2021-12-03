class Environment:
    def __init__(self, environment_json):
        self.environment_json = environment_json

    def export_environment_variables(self):
        environment = {
            'all_entity_locations': [env['position'] for env in self.environment_json],
            'all_entity_images': [env['image'] for env in self.environment_json],
            'all_entity_sizes': [env['size'] for env in self.environment_json],
            'all_entity_names':[env['name'] for env in self.environment_json],
            'mate_interactions':[],
            'attack_interactions':[],
            'healing_interactions':[],
            'up':[],
            'dn':[],
            'l':[],
            'r':[],
            'upr':[],
            'upl':[],
            'dnr':[],
            'dnl':[],
            'random':[],
            'forward':[],
            'reverse':[],
            'environment_json':self.environment_json
        }
        return environment