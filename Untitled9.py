
import requests
import pandas as pd

records=[]
headers={'access_token': 'fe66583bfe5185048c66571293e0d358'}
api_endpoint='https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales'
offset=0
limit=100
for i in range(5):
    params={'offset':offset,'limit':limit}
    response=requests.get(api_endpoint,headers=headers,params=params)
    data=response.json()
    records.extend(data["data"])
    offset+=limit

df=pd.DataFrame(records)

df['order_id'] = df['order'].apply(lambda x: x['order_id'])
df['product_id'] = df['product'].apply(lambda x: x['product_id'])
df['customer_id'] = df['order'].apply(lambda x: x['customer']['customer_id'])
df['vendor_id'] = df['order'].apply(lambda x: x['vendor']['VendorID'])
df['order_purchase_date'] = df['order'].apply(lambda x: x['order_purchase_date'])
df['order_status'] = df['order'].apply(lambda x: x['order_status'])  
df['order_delivered_customer_date'] = df['order'].apply(lambda x: x['order_delivered_customer_date']) 
df['order_estimated_delivery_date'] = df['order'].apply(lambda x: x['order_estimated_delivery_date'])
df['colors'] = df['product'].apply(lambda x: x['colors'])


df['category'] = df['product'].apply(lambda x: x['category'])
df['customer_name'] = df['order'].apply(lambda x: x['customer']['customer_name'])


df = df.drop(columns=['order','product'])

df.head()


df.replace("null",None,inplace=True)

df.isnull().sum()

duplicate_count = df.duplicated().sum()
duplicate_count


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_order'] = df['date_column'].dt.day


df = df.drop(columns=['date_column'])


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_week'] = df['date_column'].dt.dayofweek
df['day_category'] = df['day_of_week'].map({0: 'Weekday', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'})
df


df = df.drop(columns=['date_column','day_of_week'])

weekend_count = df['day_category'].value_counts().get('Weekend', 0)
weekend_count

grouped_df = df.groupby('day_category')['profit_amt'].sum()
grouped_df

grouped_d = df.groupby('category')['sales_amt'].sum()
grouped_d



