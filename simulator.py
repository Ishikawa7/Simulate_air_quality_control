import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

class Simulator():
    def __init__(self, CO = 0.03, volume = 150, people_now = 0, people_tn = [0 for i in range(10)], N_people_MA_prev_10min = 0, pumps_l_min = 200, pump_power = 0, n_pumps = 6):
        self.CO = CO
        self.volume = volume
        self.people_now = people_now
        self.people_tn = people_tn
        self.N_people_MA_prev_10min = N_people_MA_prev_10min
        self.pumps_l_min = pumps_l_min
        self.pump_power = pump_power
        self.n_pumps = n_pumps
        self.index = 0
        self.scaler = pickle.load(open('scaler.pkl', 'rb'))
        self.predict_model = tf.keras.models.load_model('predict_model.keras')

        self.columns = ['CO(mg/m^3)_initial', 'Volume(m^3)', 'N_people_MA_prev_10min',	'Ambient-Air-Pump(L/min)', 'Ambient-Air-Pump_power(%)',	'Ambient-Air-Pump_number', 'CO(mg/m^3)_final']
        self.df_sim = pd.DataFrame(columns = self.columns)
    
    def create_df_input(self, CO, volume, people_tn, pumps_l_min, pump_power, n_pumps):
        df = pd.DataFrame({
            'CO(mg/m^3)_initial':CO,
            'Volume(m^3)':volume, 
            'N_people_MA_prev_10min': sum(people_tn) / len(people_tn),	
            'Ambient-Air-Pump(L/min)': pumps_l_min, 
            'Ambient-Air-Pump_power(%)': pump_power,
            'Ambient-Air-Pump_number': n_pumps
        }, index=[self.index])
        return df

    def update_param(self, volume, people_now, pumps_l_min, pump_power, n_pumps):
        self.volume = volume
        self.people_now = people_now
        self.pumps_l_min = pumps_l_min
        self.pump_power = pump_power
        self.n_pumps = n_pumps

    def predict(self):
        df_pred = pd.DataFrame(columns = self.columns)
        index = self.index
        CO = self.CO
        for i in range(1, 11):
            index += i
            df_t = self.create_df_input(CO, self.volume, self.people_tn, self.pumps_l_min, self.pump_power, self.n_pumps, index)
            df_t_scaled = self.scaler.transform(df_t)
            df_t_scaled = pd.DataFrame(df_t_scaled, columns=self.columns[:-1])
            CO = self.model.predict(df_t_scaled)[0][0]
            #CO += (np.random.rand(1)[0]*2 -1)* 0.1278
            #if CO < 0:
            #    CO = 0
            df_t["CO(mg/m^3)_final"] = CO
            df_pred = pd.concat([df_pred,df_t])
        return df_pred[["CO(mg/m^3)_final"]]
    
    def simulate_time_step(self):
        self.people_tn.pop(0)
        self.people_tn.append(self.people_now)
        df_t = self.create_df_input(self.CO, self.volume, self.people_tn, self.pumps_l_min, self.pump_power, self.n_pumps, self.index)
        df_t_scaled = self.scaler.transform(df_t)
        df_t_scaled = pd.DataFrame(df_t_scaled, columns=self.columns[:-1])
        CO = self.model.predict(df_t_scaled)[0][0]
        CO += (np.random.rand(1)[0]*2 -1)* 0.01 * CO
        df_t["CO(mg/m^3)_final"] = CO
        self.CO = CO
        self.df_sim = pd.concat([self.df_sim,df_t])
        self.index += 1
    
    def optimize(self):
        pass

