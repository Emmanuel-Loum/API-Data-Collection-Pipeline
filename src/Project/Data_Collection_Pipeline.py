import os
import boto3
import time
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import uuid
from dotenv import load_dotenv
from collections import defaultdict
from urllib.request import urlretrieve
from tqdm import tqdm
import psycopg2
from sqlalchemy import create_engine

load_dotenv()


class API_Data:
    dir = os.getcwd()

    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.password = os.getenv('PG_PASSWORD')
        self.bucket = os.getenv('S3_BUCKET_NAME')
        self.endpoint = os.getenv('RDS_ENDPOINT')
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.parameters = {'start': '1', 'limit': '5000', 'convert': 'USD'}
        self.headers = {'Accepts': 'application/json',
                        'X-CMC_PRO_API_KEY': self.api_key}
        self.session = Session()
        global datapoint

    def retriever(self):

        '''
        Method that makes an api call to a website and extracts data
        and stores in a folder that it creates
        '''
        if os.path.isdir('raw_data'):
            pass
        else:
            os.makedirs('raw_data')  

        start_time = time.time()
        
        self.session.headers.update(self.headers)

        try:

            response = self.session.get(self.url, params=self.parameters)
            data = json.loads(response.text)
            clause = False
            global datapoint  # Makes datapoint a global variable
            datapoint = defaultdict(int)
            for i in tqdm(range(-1, (len(data['data'][0:])-1))):
                '''
                Function that creates a unique id for every datapoint
                Adds data to a dictionary
                '''
                time.sleep(0.000005)
                datapoint = data['data'][0:]
                clause = True

            if clause is True:

                path = 'raw_data'
                os.chdir(path)
                # To make a unique id using date and time 
                # timestr=datetime.now().strftime("%Y%m%d%H%M%S%")
                global uniqueid  # Create a global variable for the uniqueid
                uniqueid = uuid.uuid4() 
                '''
                creates a file and names it after the uniques id
                adds data to the created json file
                '''
                newfolder = f'{uniqueid}'
                os.makedirs(newfolder)
                with open(f'{uniqueid}/data.json', 'w') as newjfile:
                    json.dump(datapoint, newjfile)
                clause = False

        except(ConnectionError, Timeout, TooManyRedirects) as e:

            print(e)
        # To measure time complexity 
        print(f"Retrieved data .......... {(time.time()- start_time):.01f}s")

    def image_retriever(self):

        '''
        Function that retrieves images but uses a different url
        from the same website, uses datapoint from retriever method
        and changes a list to a comma separated numeric to be used
        at the id parameter as required by the website
        '''
        x_list = []
        start_time = time.time()
        for i in range(0, 50):  # no of images to be downloaded max:4001-5000
            id = datapoint[i]['id']  # Extracts the id number from datapoint
            x_list.append(id)
        x_list.sort()
        csn = ",".join(map(str, x_list))  # converts to comma-separated numeric
        k = csn[:4000]
        new_list = k.split(",")
        '''
        Uses different API url to request images
        '''
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        parameters = {
            "id": k
            # "slug":"ethereum"
            # "symbol":"ETH",
            # "address":"0xdac17f958d2ee523a2206206994597c13d831ec7",
            # "aux":"urls,logo,description,tags,platform,date_added,notice"
            }
        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            # print(data)
            '''
            Extracts the image urls and puts them in list2
            '''
            list2 = []
            for i in new_list:
                # i=str(i) -> i should a string
                x = data['data'][i]['logo']
                list2.append(x)
       
        except(ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        '''
        Function that downloads the images using urllib
        Uses unique id from retriever method to store the images 
        to the same unique id folder with the same datapoint
        '''
        mfdr = f"{uniqueid}"
        os.chdir(mfdr)
        os.makedirs('Images')
        fdr = "Images/"
        list2 = dict.fromkeys(list2)  # removes duplicate images from list 
        num = 0
        for url in (list2): 
            urlretrieve(url, fdr+os.path.basename(url))
            num += 1  # counts the number of images being downloaded
        # To measure time compleity 
        print(f"{num} images downloaded ..........{(time.time() - start_time):.01f}s")

    def upload_to_s3(self):
        '''
        Method to upload data to aws s3 for storage
        '''
        boto3.Session(aws_access_key_id = self.access_key,
        aws_secret_access_key = self.secret_key) # AWS credentials
        start_time = time.time()
        s3_client = boto3.client('s3')
        s3 = boto3.resource('s3')
        # path_dir = "/raw_data/"
        path_dir = f"{os.getcwd()}/"
        bucket_name = self.bucket
        s3_client.put_object(Bucket=bucket_name, Key=(f"{uniqueid}/"))
        os.chdir(f"{path_dir}/")
        print('uploading data...')
        s3.Bucket(bucket_name).upload_file('data.json', f"{uniqueid}/data.json")  
        # sends the data into the uuid folder
        # s3_client.put_object(Bucket=bucket_name, Key=('Images/'))  
        # creates image folder in the uuid folder
        images = f"{path_dir}/Images/"
        print('uploading images...')
        for i in os.listdir(images):  # sends every image to s3
            os.chdir(images)
            s3.Bucket(bucket_name).upload_file(f'{i}', f"{uniqueid}/Images/{i}")
        print(f"Uploaded ..........{(time.time() - start_time):.01f}s")

    def send_tabular(self):
        '''
        method that sends data to postgres database using AWS RDS
        '''
        start_time = time.time()

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = self.endpoint 
        USER ='postgres' 
        PASSWORD = self.password
        PORT = 5432
        DATABASE = 'postgres'
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect()
        print("Sending data to RDS.....wait.............")
        df = pd.DataFrame(datapoint) 
        # datapoint is inherited from retriever method above

        # datagain.drop(['platform','tags','slug'],axis=1,inplace=True)
        df['platform'] = df['platform'].astype(str)
        df['tags'] = df['tags'].astype(str)
        # converts the dtype of column to string to prevent error while sending
        df['quote'] = df['quote'].astype(str)  
        df.to_sql('crypto', engine, if_exists='replace')
        print(f"Successfully Sent ..........{(time.time() - start_time):.01f}s")


if __name__ == '__main__':
    API_Data().retriever()
    API_Data().image_retriever()
    API_Data().upload_to_s3()
    API_Data().send_tabular()
