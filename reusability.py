#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import pandas as pd


# In[ ]:





# In[ ]:





# In[ ]:





# In[4]:


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


# In[5]:


df=pd.DataFrame(records)
df


# In[6]:


df['order_id'] = df['order'].apply(lambda x: x['order_id'])
df['product_id'] = df['product'].apply(lambda x: x['product_id'])
df['customer_id'] = df['order'].apply(lambda x: x['customer']['customer_id'])
df['vendor_id'] = df['order'].apply(lambda x: x['vendor']['VendorID'])
df['order_purchase_date'] = df['order'].apply(lambda x: x['order_purchase_date'])
df['order_status'] = df['order'].apply(lambda x: x['order_status'])  
df['order_delivered_customer_date'] = df['order'].apply(lambda x: x['order_delivered_customer_date']) 
df['order_estimated_delivery_date'] = df['order'].apply(lambda x: x['order_estimated_delivery_date'])
df['colors'] = df['product'].apply(lambda x: x['colors'])


# In[7]:


df['category'] = df['product'].apply(lambda x: x['category'])
df['customer_name'] = df['order'].apply(lambda x: x['customer']['customer_name'])


# In[8]:


df['product_name'] = df['product'].apply(lambda x: x['product_name'])
df['sizes'] = df['product'].apply(lambda x: x['sizes'])


# In[9]:



df = df.drop(columns=['order','product'])
df


# In[118]:


df.head()


# In[10]:


df.replace("null",None,inplace=True)


# In[120]:


df.isnull().sum()


# In[121]:


duplicate_count = df.duplicated().sum()
duplicate_count


# In[11]:


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_order'] = df['date_column'].dt.day

df


# In[12]:


df = df.drop(columns=['date_column'])


# In[13]:


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_week'] = df['date_column'].dt.dayofweek
df['day_category'] = df['day_of_week'].map({0: 'Weekday', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'})
df


# In[14]:


df = df.drop(columns=['date_column','day_of_week'])


# In[15]:


df


# In[16]:


weekend_count = df['day_category'].value_counts().get('Weekend', 0)
weekend_count


# In[17]:


grouped_df = df.groupby('day_category')['profit_amt'].sum()
grouped_df


# In[18]:


grouped_d = df.groupby('category')['sales_amt'].sum()
grouped_d


# In[31]:


size_range=[]
for s in df["sizes"]:
    
    if(s==None):
        c=-1
    else:
        c=s.count(',')
    size_range.append(c+1)
df["size_range"]=size_range
df


# In[33]:


gf=df.sort_values('size_range',ascending=False)
gf


# In[34]:


df2=df.set_index('product_name')
df2


# In[35]:


t1=df2.loc['Mitel 5320 IP Phone VoIP phone']
t1


# In[57]:


def sizes(df,product):
    q=df.loc[product,'sizes']
    if(q.empty):
        return []
    else:
        return q
x=sizes(df2,'Howard Miller 14-1/2" Diameter Chrome Round Wal')
print(x)


# In[ ]:




