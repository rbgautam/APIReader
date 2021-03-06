import requests as rs
import time
import os
import csv
from dataaccess import read_from_csv,folder_input,init_csv
import json

folder_output = 'output/'
output_file_path = os.path.join(folder_output, init_csv("VINData"))
error_output_file_path = os.path.join(folder_output, init_csv("VINErrorData"))
def post_vin(vin):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        server = 'ievm'
        url = 'http://'+server+'.iaai.com' #base URL
        path = '/api/iaadecodevin' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd'}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = {'vin':vin,'FullDetails':1} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

def jsonify_result(df):
    new_str = df.decode('utf-8') # Decode using the utf-8 encoding
    # return json.loads(new_str.to_json(orient='records'))
    return json.dumps(new_str)

def readData():
    # List of Vins
    result = read_from_csv()
    # print(result)
    call_vin_decode(result)

def call_vin_decode(data):
    write_to_csv()
    write_to_error_csv()
    try:
        i=1
        filNum =1
        
        for vin in data:
            print(vin,',',i) 
            vin_data = post_vin(vin)
            # print("body_data:",vin_data["Body"])
            if len(vin_data["Body"]) > 0:
                body_data = vin_data["Body"][0]
                write_to_csv(vin,body_data['Model_Year'],body_data['Make'],body_data['Model'],body_data['Salvage_Type'],body_data['Body_Style_Name'],body_data['Series_Name'],body_data['EngineInformation'],body_data['Cylinders'],body_data['Fuel_Type'],body_data['Base_Shipping_Weight'],body_data['CountryOfOrigin'],body_data['Segmentation_Description'],body_data['Transmission_Type_Description'],body_data['TransmissionSpeed'],"",False)
            else:
                write_to_error_csv(vin,False)
            # print(type(body_data['Model_Year']))
            # if(i == 200):
            #    filNum = filNum +1
            #    i = 0
            #    output_file_path = output_file_path +"_"+str(filNum)
            #    error_output_file_path = error_output_file_path+"_"+str(filNum)
            i=i+1
            if i== 50:
                exit()
    except Exception as error:
        print(error)
        pass
    
       

def write_to_csv(vin="", modelyear="", makename="", modelname="", salvagetype="", bodystylename="", seriesname="", EngineInformation="", cylinders="", FuelTypeDescription="", BaseShippingWeight="", CountryOfOrigin="", SegmentationDescription="", TransmissionDescription="", TransmissionSpeed="", BlackBookValue ="", Is_Header=True ):
        # print(output_file_path)
        with open(output_file_path+".txt", mode='a',newline='') as csv_file:
                fieldnames = ["vin","modelyear","makename","modelname","salvagetype","bodystylename","seriesname","EngineInformation","cylinders","FuelTypeDescription","BaseShippingWeight","CountryOfOrigin","SegmentationDescription","TransmissionDescription","TransmissionSpeed","BlackBook Value"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [vin , modelyear , makename , modelname , salvagetype , bodystylename , seriesname , EngineInformation , cylinders , FuelTypeDescription , BaseShippingWeight , CountryOfOrigin , SegmentationDescription , TransmissionDescription , TransmissionSpeed , BlackBookValue]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)

def write_to_error_csv(vin="",Is_Header=True ):
        # print(output_file_path)
        with open(error_output_file_path+".txt", mode='a',newline='') as csv_file:
                fieldnames = ["vin"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [vin]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
readData()