import pandas as pd

class Environment:
    def __init__(self, environment_json):
        self.environment_json = environment_json
        #print(self.environment_json[0]['health'], self.environment_json[0]['energy'], self.environment_json[0]['food'], self.environment_json[0]['is_Alive'])
        # df = pd.DataFrame(self.environment_json)
        # print(df.info())