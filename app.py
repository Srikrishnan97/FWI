from flask import Flask, request, url_for, redirect, render_template
from MSCPROJ import Run
from ML_MODEL import ML
from input import Get_Inputs
import datetime
import pandas as pd
import csv
import psycopg2
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
Month = datetime.now()
Month=Month.strftime("%B")
today = datetime.today()
yesterday = today - timedelta(days=1)
td = today.strftime("%d/%m/%Y")
yd= yesterday.strftime("%d/%m/%Y")
td_date = today.strftime("%d")
td_month= today.strftime("%m")
#yd="23/08/2022"
#td="24/08/2022"
try:
    connection = psycopg2.connect(user="postgres",
                                  password="Cloud@123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="fwi")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)



def Fetch(Location):
    cursor = connection.cursor()
    cursor.execute("""SELECT FFMC,DMC,DC from FWI_DATA1 WHERE LOCATION = '"""+Location+"""' AND DATE ='"""+yd+"""'""")
    final_result =[]
    for i in cursor.fetchall():
        for j in range(0,3):
            final_result.append(i[j])
    
    FFMC_YESTERDAY=final_result[0]
    DMC_YESTERDAY=final_result[1]
    DC_YESTERDAY=final_result[2]
    #FFMC_YESTERDAY=74
    #DMC_YESTERDAY=8
    #DC_YESTERDAY=22
    #cursor.close()
    print("Fetching the yesterday's FFMC, DMC, and DC values\n")
    print("FFMC YESTERDAY:",FFMC_YESTERDAY,"\n","DMC YESTERDAY:",DMC_YESTERDAY,"\n","DC YESTERDAY:",DC_YESTERDAY,"\n")
    return(FFMC_YESTERDAY,DMC_YESTERDAY,DC_YESTERDAY)


def Calculate():
    print("________________________________________________\n")
    print("SCRAPPING ANALOG PARAMETERS FROM WEATHER STATION\n")
    print("________________________________________________\n")
    list_of_location=['Birmingham','Coventry','Dudley','Sandwell','Solihull','Walsall','Wolverhampton']
    input_list=Get_Inputs.inputs(list_of_location)

    Node_List=[]
    Readings=[]
    cursor = connection.cursor()
    #cursor.execute("""SELECT MAX(id) FROM FWI_DATA1;""")
    #select=cursor.fetchall()[0][0]
    #if(select==None):
    #    select=1
    #else:
    #    select=select+1
    #cursor.execute("""ALTER SEQUENCE fwi_data1_id_seq RESTART WITH """+str(select)+"""  ;""")

    condition="""SELECT MAX(date) FROM FWI_DATA1;"""
    cursor.execute(condition)
    date_condition=cursor.fetchall()[0][0]
    Model_Main=[]
    Model_Main2=[]
    for i in range(0,7):
        Model_List=[]
        Temperature=input_list[i][0]
        Rain=input_list[i][1]
        Relative_Humidity=input_list[i][2]
        WindSpeed=input_list[i][3]
        Prob_Rain=input_list[i][4]
        print("LOCATION :"+list_of_location[i])
        print(" TEMPERATURE :",str(Temperature)+" °C"+"\n","RELATIVE HUMIDITY :",str(Relative_Humidity)+' %'+"\n","RAIN:" , str(Rain)+" mm"+"\n","WIND SPEED :" ,str(WindSpeed)+" km/h"+"\n\n")
        print("_____________________________________________\n")
        print("CALCULATING THE FIRE WEATHER INDEX PARAMETERS\n")
        FFMC_YESTERDAY,DMC_YESTERDAY,DC_YESTERDAY=Fetch(list_of_location[i]) 
        FFMC = Run.FFMC_VALUE(FFMC_YESTERDAY,Rain,WindSpeed,Relative_Humidity,Temperature)
        DMC = Run.DMC_VALUE(DMC_YESTERDAY,Rain,Relative_Humidity,Temperature,Month)
        DC = Run.DC_VALUE(DC_YESTERDAY,Rain,Temperature,Month)
        ISI = Run.ISI_VALUE(WindSpeed,FFMC)
        BUI = Run.BUI_VALUE(DC,DMC)
        FWI = Run.FWI_VALUE(BUI,ISI)
        cursor = connection.cursor()
        print("TODAY's FWI VALUES\n")
        print(" FFMC:" ,FFMC,"\n", "DMC:" ,DMC,"\n","DC:", DC,"\n","ISI :",ISI,"\n","BUI:" ,BUI,"\n","FWI :",FWI,"\n")
        print("________________________________________________\n")
        print("CONNECTING TO PostgreSQL......\n")
        
        print("INSERTING THE DATA ACQUIRED TO DATABASE.....\n")
        print("________________________________________________\n\n")
        
        
        if(td!=date_condition):
            insert_query = """ INSERT INTO FWI_DATA1 (ID, LOCATION, DATE,TEMPERATURE,RELATIVE_HUMIDITY,RAIN,
            WIND_SPEED,FFMC,DMC,DC,ISI,BUI,FWI) VALUES (DEFAULT,'"""+list_of_location[i]+"""','"""+td+"""','"""+str(Temperature)+"""','"""+str(Relative_Humidity)+"""','"""+str(Rain)+"""'
            ,'"""+str(WindSpeed)+"""','"""+str(FFMC)+"""','"""+str(DMC)+"""','"""+str(DC)+"""','"""+str(ISI)+"""','"""+str(BUI)+"""','"""+str(FWI)+"""')"""
        else:
            insert_query="""UPDATE FWI_DATA1 SET id = DEFAULT,LOCATION='"""+list_of_location[i]+"""', DATE='"""+td+"""',TEMPERATURE='"""+str(Temperature)+"""',RELATIVE_HUMIDITY='"""+str(Relative_Humidity)+"""'
            ,RAIN='"""+str(Rain)+"""',WIND_SPEED='"""+str(WindSpeed)+"""',FFMC='"""+str(FFMC)+"""',DMC='"""+str(DMC)+"""',DC='"""+str(DC)+"""',ISI='"""+str(ISI)+"""',
            BUI='"""+str(BUI)+"""',FWI='"""+str(FWI)+"""' WHERE LOCATION='"""+list_of_location[i]+"""' AND DATE='"""+td+"""';"""
        cursor.execute(insert_query)
        connection.commit()
        Node_List.append({"FFMC":FFMC, "DMC":DMC,"DC":DC,"ISI":ISI,"BUI":BUI,"FWI":FWI})
        Readings.append({"TEMPERATURE":str(Temperature)+" °C","RELATIVE HUMIDITY":str(Relative_Humidity)+' %',"RAIN":str(Rain)+" mm","WIND SPEED":str(WindSpeed)+" km/h"})

        Model_List.append(td_date)
        Model_List.append(td_month)
        Model_List.append(Temperature)
        Model_List.append(Relative_Humidity)
        Model_List.append(Rain)
        Model_List.append(WindSpeed)
        Model_List.append(FFMC)
        Model_List.append(DMC)
        Model_List.append(DC)
        Model_List.append(ISI)
        Model_List.append(BUI)
        Model_List.append(FWI)

        Model_Main.append(Model_List)
        #Model_Main2.append(Model_Main)
    DF=pd.DataFrame(Model_Main)
    file = open('FIRE.csv', 'a+', newline ='')
    with file:   
        write = csv.writer(file)
        write.writerows(Model_Main)
    #DF.to_csv ('FIRE.csv', index=None)
    return Node_List,Readings

mylist1,Reading1=Calculate()

# sched = BackgroundScheduler(job_defaults={'max_instances': 4})
# sched.start()
# sched.add_job(lambda:Calculate(),'interval',minutes =2)
# sched.add_job(lambda:FWI(),'interval',minutes =2)

PD_LIST= pd.read_csv('FIRE.csv')
PD_LIST=PD_LIST[PD_LIST['day']==int(td_date)]
PD_LIST.to_csv ('FIRE_new.csv', index=None)

@app.route('/')
def FWI():

    mylist=mylist1
    Reading=Reading1
    #mylist=Node_List
    #Reading=Readings
    return render_template('index.html', mylist=mylist,Reading=Reading)

@app.route('/PRED/', methods=['GET', 'POST'])
def PRED():
    if request.method == 'POST':
        
        return redirect("http://127.0.0.1:5000")
    predicted_list_ML=ML.main()
    predicted_list=[]
    for i in predicted_list_ML:
        if i == 0:
            predicted_list.append("NO FIRE")
        elif i ==1:
            predicted_list.append("FIRE")
    
    return render_template('predicted.html', predicted_list=predicted_list)

# @app.route('/PRED/')

# def PRED():


#     predicted_list=ML.main()

#     return render_template('predicted.html', predicted_list=predicted_list)

if(__name__=="__main__"):
    
    
    app.run()
    
    if connection:
        connection.close()
   
    print("PostgreSQL connection is closed")
    #sched.shutdown()
    print("Today's Job Completed\n")