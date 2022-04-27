import json
from requests import Request,Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time
import uuid
import pandas as pd
import os
from dotenv import load_dotenv
from collections import defaultdict
from urllib.request import urlretrieve

load_dotenv()

from datetime import datetime


class API_Data:
    
    dir='/home/loum/Api_Data_collection/raw_data/'
    

    def  __init__(self):
        self.api_key=os.getenv('API_KEY')
        self.url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.parameters= {'start':'1','limit':'5000','convert':'USD'           }
        self.headers={ 'Accepts':'application/json', 'X-CMC_PRO_API_KEY':self.api_key}
        global datapoint
    
        

    def retriever(self):
        '''
        Makes an api call to the website
       
        '''
        start_time = time.time()
        

        session=Session()
        session.headers.update(self.headers)

        try:
            response=session.get(self.url,params=self.parameters)
            data=json.loads(response.text) 
            
            clause=False
            '''

            Makes datapoint a global variable

            '''
            global datapoint
            datapoint=defaultdict(int)

            for i in range(-1,(len(data['data'][0:])-1)): 
                i+=1 
                '''
                creates a unique id for every datapoint
                Adds data to a dictionary
                '''
                id=uuid.uuid4()

                datapoint=data['data'][0:]    
                clause=True
        
            while clause == True:
            
                path='/home/loum/Api_Data_collection/raw_data'
                os.chdir(path)
                '''
                makes a unique id using date and time
                '''
                #timestr=datetime.now().strftime("%Y%m%d%H%M%S%")
                '''
                Create a global variable for the uniqueid
                '''
                global uniqueid
                uniqueid=id
                '''
                Function that normalizes the data
                Gives the data a dataframe structure

                #xi= pd.json_normalize(data['data'])
                #df=pd.DataFrame(xi)
                #for ids in df['id']:                
                #    id=uuid.uuid4()
                #    self.d[ids]=id
                #df['id']=self.d.values()
                #print(df)
                #df.to_json("crypto.json",default_handler=str)
                '''
              
                newfolder=f'{uniqueid}'
                os.makedirs(newfolder)
                
                '''
                creates a file and names it after the uniques id
                adds data to the created json file
                '''
                with open(f'/home/loum/Api_Data_collection/raw_data/{uniqueid}/data.json','w') as newjfile:
                    json.dump(datapoint,newjfile)
                
                clause=False

        except(ConnectionError, Timeout,TooManyRedirects) as e:
            print(e)
        '''
        Measures time complexity
        '''
        print(f"Recursive Fibonacci\t --- {(time.time() - start_time):.08f} seconds ---")
    
    def image_retriever(self):


        '''
        Function that retrieves images but uses a different url 
        from the same website
        '''
        x_list=[]
        start_time = time.time()
        '''
        Extracts the id number from datapoint found in retriever method 
        in a range of numbers
        '''
        for i in range(0,50):
            id=datapoint[i]['id']
            x_list.append(id)
        '''
        changing  x_list tocomma-separated numeric to be used in id parameter
        '''
        x_list.sort()
        csn=",".join(map(str, x_list))
        k=csn[:4000]
        new_list=k.split(",")

        '''
        Different API url to request images
        '''

        url="https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"

        parameters= {
            "id":k
            #"slug":"ethereum"
            #"symbol":"ETH",
            #"address":"0xdac17f958d2ee523a2206206994597c13d831ec7",
            #"aux":"urls,logo,description,tags,platform,date_added,notice"
            }

        session=Session()
        session.headers.update(self.headers)

        try:
            response=session.get(url,params=parameters)
            data=json.loads(response.text)
            #print(data)
            '''
            Extracts the image urls and puts them in list2
            '''
            list2=[]
            for  i in new_list:
                #i=str(i) -> i should a string
                x=data['data'][i]['logo']
                list2.append(x)

            #print(list2)          
        except(ConnectionError, Timeout,TooManyRedirects) as e:
            print(e)
        
        '''
        Downloads the images using urllib
        Uses unique id from retriever method to store the images to the same unique id folder
        with the same datapoint
        '''
        mfdr=f"/home/loum/Api_Data_collection/raw_data/{uniqueid}/"
        os.chdir(mfdr)
        os.makedirs('Images')
        fdr=f"/home/loum/Api_Data_collection/raw_data/{uniqueid}/Images/"
        for url in list2:

            urlretrieve(url, fdr+os.path.basename(url))
            pass
            
            '''
            Measures time complexity
            '''   
            print(f"Recursive Fibonacci\t --- {(time.time() - start_time):.08f} seconds ---")

        #print(f"Recursive Fibonacci\t --- {(time.time() - start_time):.08f} seconds ---")
 
if __name__=='__main__':

    API_Data().retriever()
    API_Data().image_retriever()