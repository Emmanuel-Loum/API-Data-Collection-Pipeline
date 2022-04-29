# API DATA COLLECTION PIPELINE
____

## Milestone 1

Collects json data from [CoinMarketCap](https://coinmarketcap.com/api/API)   website 

##  Milestone 2

Creates a class named *API_Data* and method *retriever* to push requests to the API and pull the required data using an api key generated from [CoinMarketCap](https://coinmarketcap.com/api/API) 


```python

class API_Data:
    

    def  __init__(self):
        self.api_key=os.getenv('API_KEY')
        self.url="https://pro-api.coinmarketcap.com/v1cryptocurrency/listings/latest"
        self.parameters= {'start':'1','limit':'5000','convert':'USD'}
        self.headers={'Accepts':'application/json', 'X-CMC_PRO_API_KEY':self.api_key}
        self.datad={}
        
    def retriever(self):
        
        session=Session()
        session.headers.update(self.headers)
        pass
        try:
            self.response=session.get(self.url,params=self.parameters)
            data=json.loads(self.response.text) 
            print(data['data'][0].keys())

        except(ConnectionError, Timeout,TooManyRedirects) as e:
            print(e)

    if __name__=='__main__':
    API_Data().retriever()

```
## Milestone 3
### Retriever method
______
Generates a v4 UUID to be assigned as a global unique ID for each datapoint entry/request and names a new folder created

```python
                
uniqueid=uuid.uuid4()

newfolder=f'{uniqueid}'
os.makedirs(newfolder)
            

```
Creates a json file named data and dumps the extracted data
```python
  with open(f'/home/loum/Api_Data_collection/raw_data/{uniqueid}/data.json','w') as newjfile:
                    json.dump(datapoint,newjfile)
```

### Image_retriever method
____
*Image_retriever* method extracts images from the same website but uses a different url thus use of a different api from the *retriever* method

```python
url="https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"

```

<!--Blockquote-->
>Image_retriever method inherits *datapoint*  from retriever method to extract id for the each image to be used at theid parameter


Range of number of ids to be extracted
```python
for i in range(0,50):
            id=datapoint[i]['id']
            x_list.append(id)
```


 Format the list to a comma separated numeric as required for the id parameter

```python
        x_list.sort()
        csn=",".join(map(str, x_list))
        k=csn[:4000]
        csn_list=k.split(",")

                url

        parameters= {
            "id":k
        }
```
uses inherited uniqueid to save the images in a created dir *Images* next to data json file in uniqueid folder a
```python
 mfdr=f"/home/loum/Api_Data_collection/raw_data/{uniqueid}/"
        os.chdir(mfdr)
        os.makedirs('Images')
        fdr=f"/home/loum/Api_Data_collection/raw_data/{uniqueid}/Images/"

```



Extracts url link from the data retrieved and through urllib library, 
downloads and stores each image in Image file fusing 
 ```python
        list2=[]
            for  i in csn_list:
                #i=str(i) -> i should a string
                x=data['data'][i]['logo']
                list2.append(x) 


        for url in list2:

            urlretrieve(url, fdr+os.path.basename(url))
            pass
            
```







