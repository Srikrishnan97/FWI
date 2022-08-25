#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class Run :
    global FFMC_Calculation
    def FFMC_Calculation(RC,RelativeHumidity,WindSpeed,Temperature):
        if(Temperature <= 5):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout.csv')
        elif((Temperature >= 5.5) & (Temperature<=10)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout1.csv')
        elif((Temperature >= 10.5) & (Temperature<=15)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout2.csv')
        elif((Temperature >= 15.5) & (Temperature<=20)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout3.csv')
        elif((Temperature >= 20.5) & (Temperature<=25)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout4.csv')
        elif((Temperature >= 25.5) & (Temperature<=30)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout5.csv')
        elif((Temperature >= 30.5) & (Temperature<=35)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout6.csv')
        elif((Temperature >= 35.5)):
            FFMC = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMC_NO_RAINout7.csv')
        else:
            print("Temperature Not Found")
        FFMC_dict = {'RC0': [0, 2] , 'RC1' : [3, 7] , 'RC2' : [8, 12] , 'RC3' : [13, 17], 'RC4' : [18, 22], 
            'RC5': [23, 27] , 'RC6' : [28, 32] , 'RC7' : [33, 37], 'RC8' : [38, 42], 'RC9' : [43, 47],
            'RC10': [48, 52] , 'RC11' : [53, 57] , 'RC12' : [58, 62], 'RC13' : [63, 67], 
            'RC14' : [68, 72], 'RC15': [73, 77] , 'RC16' : [78, 79] , 'RC17' : [80,80] , 
            'RC18' : [81,81], 'RC19' : [82,82], 'RC20': [83,83] , 'RC21' : [84,84] , 'RC22' : [85,85], 
            'RC23' : [86,86], 'RC24' : [87,87],'RC25': [88,88],'RC26' : [89,89] , 'RC27' : [90,90], 
            'RC28' : [91,91],'RC29' : [92,92], 'RC30' : [93,93] , 'RC31' : [94,94], 'RC32' : [95,95], 
            'RC33' : [96,96], 'RC34' : [97,97] , 'RC35' : [98,98], 'RC36' : [99,99]
        }

        RH_val = ['0-10','11-18','19-28','29-38','39-49','50-61','62-73','74-84','85-93','94-100']
        R=[RH_val[i//4] for i in range(0,40)]
        FFMC['RH'] = R
        FFMC['LowerRH'], FFMC['UpperRH'] = FFMC['RH'].str.split('-', 1).str
        wind ={
        'A':[0,3], 'B':[4,13], 'C':[14,28],'D' :[29,300]
        }

        FFMC['Wind'] = FFMC['Level'].map(wind)
        FFMC1 = pd.DataFrame(FFMC['Wind'].to_list(), columns=['LowerWind','UpperWind'])
        FFMC1
        numbers = FFMC1['LowerWind']
        FFMC = FFMC.join(numbers)
        numbers1 = FFMC1['UpperWind']
        FFMC = FFMC.join(numbers1)
        convert_dict = {'LowerRH': int,
                    'UpperRH': int
                    }
        FFMC = FFMC.astype(convert_dict)
        
        FFMC1 = FFMC[(FFMC['LowerRH'] <= RelativeHumidity) & 
                        ((FFMC['UpperRH'] >= RelativeHumidity))]
        FFMC2 = FFMC1[(FFMC1['LowerWind'] <= WindSpeed) & 
                        ((FFMC['UpperWind'] >= WindSpeed))] 
        for k,v in FFMC_dict.items():
            if((RC>=v[0]) and (RC <=v[1])):
                YesCode=k
            elif(RC==v[0]):
                YesCode=k
        FFMC3 = FFMC2[(FFMC1['LowerWind'] <= WindSpeed) & 
                        ((FFMC['UpperWind'] >= WindSpeed))]

        FFMC3=FFMC2[YesCode].values
        return FFMC3[0]

    
    def FFMC_VALUE(FFMC_Yesterday, Rain, Windspeed, RH,Temperature):
        
        if (Rain > 0.5 ):
            RainCode=pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FFMCout.csv')
        #FFMC TABLE 1 CALCULATION (RAIN YES)
            RC_dict = {'R1': [0.0,0.5] , 'R1' : [0.6,0.7] , 'R2' : [0.8,0.9] , 'R3' : [1.0,1.1], 'R4' : [1.2,1.3], 
            'R5': [1.4,1.5] , 'R6' : [1.6,1.7] , 'R7' : [1.8,2.0], 'R8' : [2.1,2.3], 'R9' : [2.4,2.6],
            'R10': [2.7,2.9] , 'R11' : [3.0,3.2] , 'R12' : [3.3,3.5], 'R13' : [3.6,3.9], 
            'R14' : [4.0,4.4], 'R15': [4.5,5.0] , 'R16' : [5.1,5.7] , 'R17' : [5.8,6.6] , 
            'R18' : [6.7,7.7], 'R19' : [7.8,9.1], 'R20': [9.2,11.5] , 'R21' : [11.6,14.5] , 
            'R22' : [14.6,17.5], 'R23' : [17.6,21.5], 'R24' : [21.6,25.5],'R25': [25.6,30.5],
            'R26' : [30.6,37.5] , 'R27' : [37.6,46.5], 'R28' : [46.5,58.5], 'R29' : [59.6,100]
            }
            RainCode['LowerFFMC'], RainCode['UpperFFMC'] = RainCode['FFMC'].str.split('-', 1).str
            RainCode['UpperFFMC'] = RainCode['UpperFFMC'].replace(np.nan, 0)
            RainCode.UpperFFMC[RainCode.UpperFFMC == 0] = RainCode.LowerFFMC
            for k,v in RC_dict.items():
                if((Rain>=v[0]) and (Rain <=v[1])):
                    raincode=k
            convert_dict = {'LowerFFMC': int,
                    'UpperFFMC': int
                    }
            RainCode = RainCode.astype(convert_dict)
            RainCode1 = RainCode[(RainCode['LowerFFMC'] <= FFMC_Yesterday) & 
                        ((RainCode['UpperFFMC'] >= FFMC_Yesterday))]

            RC=RainCode1[raincode].values
            Raincode=RC[0]
            Today_FFMC_Value=FFMC_Calculation(Raincode,RH, Windspeed,Temperature)
            #print(Today_FFMC_Value)
        else:
            Today_FFMC_Value=FFMC_Calculation(FFMC_Yesterday, RH, Windspeed, Temperature)
            #print(Today_FFMC_Value)
        return Today_FFMC_Value

    global DMC_Calculation
    def DMC_Calculation(RC,Month,RelativeHumidity,Temperature):
        DMC_DF = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\DMC_NO_RAINout.csv')
        DMC_DF['LowerRH'], DMC_DF['UpperRH'] = DMC_DF['RH'].str.split('-', 1).str
        DMC_DF['LowerTemp'], DMC_DF['UpperTemp'] = DMC_DF['Temperature'].str.split('-', 1).str
        convert_dict = {'LowerRH': int,
                    'UpperRH': int,
                    'LowerTemp' : float,
                    'UpperTemp' : float
                    }
        DMC_DF = DMC_DF.astype(convert_dict)
        DMC_DryingFactor = DMC_DF[(DMC_DF['LowerRH'] <= RelativeHumidity) & 
                        ((DMC_DF['UpperRH'] >= RelativeHumidity))]
        DMC_DryingFactor2 = DMC_DryingFactor[(DMC_DryingFactor['LowerTemp'] <= Temperature) & 
                        ((DMC_DryingFactor['UpperTemp'] >= Temperature))] 
        if(Month == 'January' or Month == 'December'):
            DMC_DryingFactor3 = 0
        else:
            DMC_DryingFactor3 = DMC_DryingFactor2[Month].values
            DMC_DryingFactor3=DMC_DryingFactor3[0]
        TodayDMC= DMC_DryingFactor3 + RC
        return TodayDMC

    def DMC_VALUE(DMC_Yesterday,Rain,RelativeHumidity,Temperature,Month):
        if(Rain>=1.4):
    
            DMC_Rain = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\DMCout.csv')
            #print(DMC_Rain)
            DMC_Rain['LowerDMC'], DMC_Rain['UpperDMC'] = DMC_Rain['DMC'].str.split('-', 1).str
            DMC_dict = {'MM1' : [1.5, 1.6] , 'MM2' : [1.7, 1.8] , 'MM3' : [1.9, 2.0], 
                'MM4' :[2.1,2.2],'MM5': [2.3, 2.5] , 'MM6' : [2.6, 2.8] , 'MM7' : [2.9, 3.1], 
                'MM8' : [3.2, 3.4], 'MM9' : [3.5, 3.8],'MM10': [3.9,4.2] , 'MM11' : [4.3, 4.6] , 
                'MM12' : [4.7, 5.1], 'MM13' : [5.2,5.7],'MM14' : [5.8,6.4], 'MM15': [6.5,7.2] , 
                'MM16' : [7.3,8.2] , 'MM17' : [8.3,9.4] ,'MM18' : [9.5,11.5], 'MM19' : [11.6,14.5], 
                'MM20': [14.6,17.5] ,'MM21' : [17.6,20.5] , 'MM22' : [20.6,24.5],
                'MM23' : [24.6,28.5], 'MM24' : [28.6,33.5],'MM25': [33.6,39.5],
                'MM26' : [39.6,47.5] , 'MM27' : [47.6,59.5], 'MM28': [59.6,79.5],'MM29': [79.6,200]
            }
            for k,v in DMC_dict.items():
                if((Rain>=v[0]) and (Rain <=v[1])):
                    raincode=k
            convert_dict = {'LowerDMC': int,
                        'UpperDMC': int
                    }
            DMC_Rain = DMC_Rain.astype(convert_dict)
            DMC_Rain1 = DMC_Rain[(DMC_Rain['LowerDMC'] <= DMC_Yesterday) & 
                        ((DMC_Rain['UpperDMC'] >= DMC_Yesterday))]
            RC_DMC=DMC_Rain1[raincode].values
            Raincode=RC_DMC[0]
            Today_DMC_Value=DMC_Calculation(Raincode,Month,RelativeHumidity,Temperature)
            #print(Today_DMC_Value)
        else:
            Today_DMC_Value=DMC_Calculation(DMC_Yesterday,Month,RelativeHumidity,Temperature)
            #print(Today_DMC_Value)
        return Today_DMC_Value

    global DC_Calculation
    def DC_Calculation(RC,Temperature,Month):
        DC_DF = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\DC_NO_RAINout.csv')
        DC_DF['LowerTemp'], DC_DF['UpperTemp'] = DC_DF['Temperature'].str.split('-', 1).str
        convert_dict = {
                    'LowerTemp' : float,
                    'UpperTemp' : float
                    }
        DC_DF = DC_DF.astype(convert_dict)
        
        DC_DryingFactor = DC_DF[(DC_DF['LowerTemp'] <= Temperature) & 
                        ((DC_DF['UpperTemp'] >= Temperature))] 

        DC_DryingFactor = DC_DryingFactor[Month].values
        DC_DryingFactor=DC_DryingFactor[0]
        TodayDC= DC_DryingFactor + RC
        return TodayDC

    def DC_VALUE(DC_Yesterday,Rain,Temperature,Month):
        if(Rain>2.8):
            DC_Rain = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\DCout.csv')
            DC_Rain['LowerDC'], DC_Rain['UpperDC'] = DC_Rain['DC'].str.split('-', 1).str
            DC_dict = {'M1' : [2.9, 4.6] , 'M2' : [4.7, 6.2] , 'M3' : [6.3, 7.8], 
                'M4' :[7.9,9.4],'M5': [9.5,11.5] , 'M6' : [11.6,13.5] , 'M7' : [13.6,15.5], 
                'M8' : [15.6,18.5], 'M9' : [18.6,21.5],'M10': [21.6,25.5] , 'M11' : [25.6,30.5] , 
                'M12' : [30.6,35.5], 'M13' : [35.6,40.5],'M14' : [40.6,45.5], 'M15': [45.6,50.5] , 
                'M16' : [50.6,55.5] , 'M17' : [55.6,60.5] ,'M18' : [60.6,65.5], 'M19' : [65.6,70.5], 
                'M20': [70.6,75.5] ,'M21' : [75.6,80.5] , 'M22' : [80.6,85.5],
                'M23' : [85.6,90.5], 'M24' : [90.6,95.5],'M25': [95.6,100.5],
                'M26' : [100.6,105.5] , 'M27' : [105.6,2000]
            }
            for k,v in DC_dict.items():
                if((Rain>=v[0]) and (Rain <=v[1])):
                    raincode=k
            convert_dict = {'LowerDC': int,
                    'UpperDC': int
                    }
            DC_Rain = DC_Rain.astype(convert_dict)
            DC_Rain1 = DC_Rain[(DC_Rain['LowerDC'] <= DC_Yesterday) & 
                        ((DC_Rain['UpperDC'] >= DC_Yesterday))]
            RC_DC=DC_Rain1[raincode].values
            Raincode=RC_DC[0]
            Today_DC_Value=DC_Calculation(Raincode,Temperature,Month)
            
        else:
            Today_DC_Value=DC_Calculation(DC_Yesterday,Temperature,Month)
            
        return Today_DC_Value

    def ISI_VALUE(WindSpeed,Today_FFMC_Value):
        ISI = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\ISIout.csv')
        ISI_dict = {'FFMC1'  : [0, 32] , 'FFMC2' : [33,37] , 'FFMC3' : [38,42], 
                'FFMC4' : [43,47] ,'FFMC5': [48,52] , 'FFMC6' : [53,57] , 'FFMC7' : [58,62], 
                'FFMC8' : [63,67], 'FFMC9' : [68,72],'FFMC10': [73,77] , 'FFMC11' : [78,79] , 
                'FFMC12': [80,80], 'FFMC13' : [81,81],'FFMC14' : [82,82], 'FFMC15': [83,83] , 
                'FFMC16': [84,84] , 'FFMC17' : [85,85] ,'FFMC18' : [86,86], 'FFMC19' : [87,87], 
                'FFMC20': [88,88] ,'FFMC21' : [89,89] , 'FFMC22' : [90,90],
                'FFMC23': [91,91], 'FFMC24' : [92,92],'FFMC25': [93,93],
                'FFMC26': [94,94] , 'FFMC27' : [95,95], 'FFMC28':[96,96], 
                'FFMC29' :[97,97], 'FFMC30' :[98,98],'FFMC31': [99,99]
        }
        for k,v in ISI_dict.items():
            if((Today_FFMC_Value>=v[0]) and (Today_FFMC_Value <=v[1])):
                ISI_Code=k
        new_wind=round(WindSpeed)
        ISI=ISI[ISI['Wind']==WindSpeed][ISI_Code].values
        Today_ISI_Value=ISI[0]
        return Today_ISI_Value

    def BUI_VALUE(Today_DC_Value,Today_DMC_Value):
        BUI = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\BUI.csv')
        BUI['LowerDMC'], BUI['UpperDMC'] = BUI['DMC'].str.split('-', 1).str
        BUI['UpperDMC'] = BUI['UpperDMC'].replace(np.nan, 0)
        BUI.UpperDMC[BUI.UpperDMC == 0] = BUI.LowerDMC
        BUI_dict = {'DC1'  : [0, 19] , 'DC2' : [20,39] , 'DC3' : [40,59], 
                'DC4' : [60,79] ,'DC5': [80,99] , 'DC6' : [100,119] , 'DC7' : [120,139], 
                'DC8' : [140,159], 'DC9' : [160,179],'DC10': [180,199] , 'DC11' : [200,224] , 
                'DC12': [225,249], 'DC13' : [250,274],'DC14' : [275,299], 'DC15': [300,329] , 
                'DC16': [330,359] , 'DC17' : [360,399] ,'DC18' : [400,439], 'DC19' : [440,489], 
                'DC20': [490,539] ,'DC21' : [540,599] , 'DC22' : [600,659],
                'DC23': [660,729], 'DC24' : [730,809],'DC25': [810,899],
                'DC26': [900,999] , 'DC27' : [1000,1099], 'DC28':[1100,1199]
        }

        for k,v in BUI_dict.items():
            if((Today_DC_Value>=v[0]) and (Today_DC_Value <=v[1])):
                BUI_Code=k

        convert_dict = {'LowerDMC': int,
                    'UpperDMC': int
                    }
        BUI = BUI.astype(convert_dict)
        BUI = BUI[(BUI['LowerDMC'] <= Today_DMC_Value) & 
                        ((BUI['UpperDMC'] >= Today_DMC_Value))]
        Today_BUI_Value = BUI[BUI_Code].values
        Today_BUI_Value=Today_BUI_Value[0]
        
        return Today_BUI_Value


    def FWI_VALUE(Today_BUI_Value,Today_ISI_Value):
        FWI = pd.read_csv(r'C:\Users\Krishna\Desktop\Datasets\FWI.csv')
        FWI['LowerISI'], FWI['UpperISI'] = FWI['ISI'].str.split('-', 1).str
        FWI['UpperISI'] = FWI['UpperISI'].replace(np.nan, 0)
        FWI.UpperISI[FWI.UpperISI==0]=FWI.LowerISI
        FWI_dict = {'BUI1'  : [0, 1] , 'BUI2' : [2,3] , 'BUI3' : [4,5], 
                    'BUI4' : [6,7] ,'BUI5': [8,9] , 'BUI6' : [10,11] , 'BUI7' : [12,14], 
                    'BUI8' : [15,17], 'BUI9' : [18,20],'BUI10': [21,23] , 'BUI11' : [24,26] , 
                    'BUI12': [27,30], 'BUI13' : [31,34],'BUI14' : [35,38], 'BUI15': [39,42] , 
                    'BUI16': [43,47] , 'BUI17' : [48,52] ,'BUI18' : [53,57], 'BUI19' : [58,63], 
                    'BUI20': [64,69] ,'BUI21' : [70,75] , 'BUI22' : [76,82],
                    'BUI23': [83,89], 'BUI24' : [90,97],'BUI25': [98,106],
                    'BUI26': [107,116] , 'BUI27' : [117,128], 'BUI28':[129,142], 
                    'BUI29':[143,159],'BUI30':[160,180],'BUI31':[181,206],'BUI32':[207,238],
                    'BUI33':[239,277],'BUI34':[278,324],'BUI35':[325,381],'BUI36':[382,1000]
            }

        for k,v in FWI_dict.items():
                if((Today_BUI_Value>=v[0]) and (Today_BUI_Value <=v[1])):
                    FWI_Code=k
        convert_dict = {'LowerISI': float,
                        'UpperISI': float
                        }
        FWI = FWI.astype(convert_dict)

        FWI = FWI[(FWI['LowerISI'] <= Today_ISI_Value) & 
                            ((FWI['UpperISI'] >= Today_ISI_Value))]
        FWI = FWI[FWI_Code].values
        Today_FWI_Value=FWI[0]
        return Today_FWI_Value