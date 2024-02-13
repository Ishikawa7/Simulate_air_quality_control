import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

class Simulator():
    def __init__(self, CO = 0.015, volume = 20, people_now = 0, people_tn = [0 for i in range(3)],
                  N_people_MA_prev_10min = 0, pumps_l_min = 680, pump_power = 0, n_pumps = 8, threshold = 1.0):
        self.CO = CO
        self.volume = volume
        self.people_now = people_now
        self.people_tn = people_tn
        self.N_people_MA_prev_10min = N_people_MA_prev_10min
        self.pumps_l_min = pumps_l_min
        self.pump_power = pump_power
        self.n_pumps = n_pumps
        self.threshold = threshold
        self.index = 0
        self.scaler = pickle.load(open('scaler.pkl', 'rb'))
        self.predict_model = tf.keras.models.load_model('predict_model.keras')
        self.predictions = [0 for i in range(10)]

        self.columns = ['CO(mg/m^3)_initial', 'Volume(m^3)', 'N_people_MA_prev_10min',	'Ambient-Air-Pump(L/min)',
                         'Ambient-Air-Pump_power(%)',	'Ambient-Air-Pump_number', 'CO(mg/m^3)_final']
        self.df_sim = pd.DataFrame(columns = self.columns)

        self.active = True
    
    def modell_call(self, CO, volume, people_tn, pumps_l_min, pump_power, n_pumps, index):
        df_t = pd.DataFrame({
            'CO(mg/m^3)_initial':CO,
            'Volume(m^3)':volume, 
            'N_people_MA_prev_10min': sum(people_tn) / len(people_tn),	
            'Ambient-Air-Pump(L/min)': pumps_l_min, 
            'Ambient-Air-Pump_power(%)': pump_power,
            'Ambient-Air-Pump_number': n_pumps
        }, index=[index])
        df_t_scaled = self.scaler.transform(df_t)
        df_t_scaled = pd.DataFrame(df_t_scaled, columns=self.columns[:-1])
        CO_new = self.predict_model.predict(df_t_scaled, verbose = 0)[0][0]
        df_t["CO(mg/m^3)_final"] = CO_new
        return df_t
    
    def predict(self, initial_CO, pump_power):
        #print("CALL PREDICT")
        index = self.index
        CO = initial_CO
        for i in range(1, 11):
            index += i
            df_t = self.modell_call(CO, self.volume, self.people_tn, self.pumps_l_min, pump_power, self.n_pumps, index)
            CO = df_t['CO(mg/m^3)_final'].values[0]
            if i == 1:
                df_pred = df_t
            else:
                df_pred = pd.concat([df_pred,df_t])
        return df_pred[["CO(mg/m^3)_final"]].values
    
    def optimize(self, predictions):
        #print("CALL OPTIMIZE")
        best_pump_power = self.pump_power
        best_result = 9999
        best_predictions = 0
        for power in range(0,120,20):
            result = 0
            predictions = self.predict(self.CO, power)
            for pred in predictions:
                if pred > self.threshold:
                    result += pred - self.threshold
            if result < best_result:
                best_result = result
                best_pump_power = power
                best_predictions = predictions
        self.predictions = best_predictions.flatten()
        return best_pump_power
    
    def simulate_time_step(self):
        #print("CALL SIMULATE TIME STEP: index = ", self.index)
        self.people_tn.pop(0)
        self.people_tn.append(self.people_now)

        self.pump_power = self.optimize(self.predict(self.CO, self.pump_power))

        df_new = self.modell_call(self.CO, self.volume, self.people_tn, self.pumps_l_min, self.pump_power, self.n_pumps, self.index)
        df_new['CO(mg/m^3)_final'] += (np.random.rand(1)[0]*2 -1)* 0.01 * df_new['CO(mg/m^3)_final']
        self.CO = df_new['CO(mg/m^3)_final'].values[0]
        self.df_sim = pd.concat([self.df_sim,df_new])
        self.index += 1