import pickle
import pandas as pd
from sklearn import neural_network, linear_model, preprocessing, svm, tree
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
import warnings

class ML:

    def main():
        with open("model_pkl.pkl",'rb') as file:
            mp=pickle.load(file)
        warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
        #forestfire=pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\DATASET\FIREC.csv')
        forestfire=pd.read_csv('FIRE_new.csv')
        forest_fires=forestfire
        month_values = list(forest_fires['month'])
        day_values = list(forest_fires['day'])
        ffmc_values = list(forest_fires['FFMC'])
        dmc_values = list(forest_fires['DMC'])
        dc_values = list(forest_fires['DC'])
        isi_values = list(forest_fires['ISI'])
        temp_values = list(forest_fires['temp'])
        rh_values = list(forest_fires['RH'])
        wind_values = list(forest_fires['wind'])
        rain_values = list(forest_fires['rain'])
        #bui_values = list(forest_fires['BUI'])
        #fwi_values = list(forest_fires['FWI'])
        area_values = list(forest_fires['FIRE'])
        attribute_list = []
    
        Length = list(forestfire['temp'])
        for index in range(0, len(Length)):
            temp_list = []
            
            temp_list.append(month_values[index])
            temp_list.append(day_values[index])
            temp_list.append(ffmc_values[index])
            temp_list.append(dmc_values[index])
            temp_list.append(dc_values[index])
            temp_list.append(isi_values[index])
            #temp_list.append(bui_values[index])
            #temp_list.append(fwi_values[index])
            temp_list.append(temp_values[index])
            temp_list.append(rh_values[index])
            temp_list.append(wind_values[index])
            temp_list.append(rain_values[index])
            attribute_list.append(temp_list)
        
        # attribute_list=[[8, 1, 92.1, 207.0, 672.6, 8.2, 26.8, 35, 1.3, 0.0],
        # [8, 6, 93.7, 231.1, 715.1, 8.4, 18.9, 64, 4.9, 0.0],[8, 4, 91.6, 248.4, 753.8, 6.3, 16.6, 59, 2.7, 0.0],
        # [9, 5, 92.1, 99.0, 745.3, 9.6, 20.8, 35, 4.9, 0.0],[9, 5, 91.1, 91.3, 738.1, 7.2, 20.7, 46, 2.7, 0.0],
        # [9, 3, 92.9, 133.3, 699.6, 9.2, 26.4, 21, 4.5, 0.0],
        # [9, 2, 91.0, 129.5, 692.6, 7.0, 18.3, 40, 2.7, 0.0],
        # [6, 5, 92.5, 56.4, 433.3, 7.1, 23.2, 39, 5.4, 0.0],
        # [6, 5, 92.5, 56.4, 433.3, 7.1, 23.2, 39, 5.4, 0.0]]

        
        predicted_y = mp.predict(attribute_list)
        print(predicted_y.tolist())
        return predicted_y
