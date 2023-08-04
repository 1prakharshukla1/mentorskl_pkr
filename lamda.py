#!/usr/bin/env python
# coding: utf-8

# In[52]:


import requests
import pandas as pd
import os 
from dotenv import load_dotenv

load_dotenv()

access_token=os.getenv('acess token')

# In[ ]:





# In[ ]:





# In[ ]:





# In[53]:


records=[]
headers={'access_token': access_token}
api_endpoint='https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales'
offset=0
limit=100
for i in range(5):
    params={'offset':offset,'limit':limit}
    response=requests.get(api_endpoint,headers=headers,params=params)
    data=response.json()
    records.extend(data["data"])
    offset+=limit


# In[54]:


records


# In[55]:


df=pd.DataFrame(records)
df


# In[56]:


df['order_id'] = df['order'].apply(lambda x: x['order_id'])
df['product_id'] = df['product'].apply(lambda x: x['product_id'])
df['customer_id'] = df['order'].apply(lambda x: x['customer']['customer_id'])
df['vendor_id'] = df['order'].apply(lambda x: x['vendor']['VendorID'])
df['order_purchase_date'] = df['order'].apply(lambda x: x['order_purchase_date'])
df['order_status'] = df['order'].apply(lambda x: x['order_status'])  
df['order_delivered_customer_date'] = df['order'].apply(lambda x: x['order_delivered_customer_date']) 
df['order_estimated_delivery_date'] = df['order'].apply(lambda x: x['order_estimated_delivery_date'])
df['colors'] = df['product'].apply(lambda x: x['colors'])


# In[57]:


df['vendor_name'] = df['order'].apply(lambda x: x['vendor']['VendorID'])


# In[58]:


df['category'] = df['product'].apply(lambda x: x['category'])
df['customer_name'] = df['order'].apply(lambda x: x['customer']['customer_name'])


# In[59]:


df['product_name'] = df['product'].apply(lambda x: x['product_name'])
df['sizes'] = df['product'].apply(lambda x: x['sizes'])


# In[60]:



df = df.drop(columns=['order','product'])
df


# In[61]:


df.head()


# In[62]:


df.replace("null",None,inplace=True)


# In[63]:


df.isnull().sum()


# In[64]:


duplicate_count = df.duplicated().sum()
duplicate_count


# In[65]:


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_order'] = df['date_column'].dt.day

df


# In[66]:


df = df.drop(columns=['date_column'])


# In[67]:


df['date_column'] = pd.to_datetime(df['order_purchase_date'])
df['day_of_week'] = df['date_column'].dt.dayofweek
df['day_category'] = df['day_of_week'].map({0: 'Weekday', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'})
df


# In[68]:


df = df.drop(columns=['date_column','day_of_week'])


# In[69]:


df


# In[70]:


weekend_count = df['day_category'].value_counts().get('Weekend', 0)
weekend_count


# In[71]:


grouped_df = df.groupby('day_category')['profit_amt'].sum()
grouped_df


# In[72]:


grouped_d = df.groupby('category')['sales_amt'].sum()
grouped_d


# In[73]:


size_range=[]
for s in df["sizes"]:
    
    if(s==None):
        c=-1
    else:
        c=s.count(',')
    size_range.append(c+1)
df["size_range"]=size_range
df


# In[74]:


gf=df.sort_values('size_range',ascending=False)
gf


# In[75]:


df2=df.set_index('product_name')
df2


# In[76]:


t1=df2.loc['Mitel 5320 IP Phone VoIP phone']
t1


# In[ ]:





# In[ ]:





# In[77]:


df['order_purchase_date'] = pd.to_datetime(df['order_purchase_date'])

# Use a lambda function to get the month name from 'order_purchase_date'
df['order_purchase_month'] = df['order_purchase_date'].apply(lambda x: x.strftime('%B'))
df


# In[78]:


gp=df.groupby('order_purchase_month')['sales_amt'].sum()
gp=gp.sort_values(ascending=False)
gp


# In[79]:


gp2=df.groupby('order_purchase_month')['profit_amt'].sum()
gp2=gp2.sort_values(ascending=False)
gp2


# In[80]:


df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])

# Calculate the difference in hours between the two dates
df['delivery_time_hours'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.total_seconds() / 3600
df


# In[81]:


df['delivery_staus']=df['delivery_time_hours'].apply(lambda x: 'late' if x > 0 else 'ontime')
df


# In[82]:


gp3=df.groupby('delivery_staus')['delivery_staus'].count()
gp3


# In[83]:



df


# In[88]:


result = df.groupby(['vendor_id', 'delivery_staus']).agg(delivery_status_count=('delivery_staus', 'count')).reset_index()
result


# In[ ]:




