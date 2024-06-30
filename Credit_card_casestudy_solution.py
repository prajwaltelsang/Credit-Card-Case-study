#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing the packages
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


cust=pd.read_csv("Customer Acqusition.csv")


# In[3]:


spend=pd.read_csv("spend.csv")


# In[4]:


repay=pd.read_csv("Repayment.csv")


# In[5]:


cust.drop(columns =['No'],axis=1,inplace=True)


# In[6]:


spend.drop(columns=['Sl No:'],axis=1,inplace=True)


# In[7]:


repay.drop(columns=['SL No:','Unnamed: 4'],axis=1,inplace=True)


# In[8]:


cust.head()


# In[9]:


spend.head()


# In[10]:


repay.head()


# In[11]:


cust.shape


# In[12]:


spend.shape


# In[13]:


repay.shape


# In[14]:


cust.dtypes


# In[15]:


repay.dtypes


# In[16]:


spend.dtypes


# In[17]:


cust.isnull().sum()


# In[18]:


repay.isnull().sum()


# In[19]:


spend.isnull().sum()


# In[20]:


repay.dropna(inplace=True)


# In[21]:


repay.isnull().sum()



# 1.(a)In case age is less than 18, replace it with mean of age values.

# In[22]:


cust['Age'].mean()


# In[23]:


cust.loc[cust['Age']<18,"Age"] = cust["Age"].mean()


# In[24]:


mean_new = cust["Age"].mean()


# In[25]:


mean_new


# In[26]:


print("All the customers who have age less than 18 have been replaced by mean of the age column.")


# (b) In case spend amount is more than the limit,replace it with 50% of that customer limit.

# In[27]:


cust.head(1)


# In[28]:


spend.head(1)


# In[29]:


cust_spend = pd.merge(left=cust,right=spend,how="inner",left_on="Customer",right_on="Customer")


# In[30]:


cust_spend.head()


# In[31]:


cust_spend.shape


# In[32]:


cust_spend.loc[cust_spend['Amount']>cust_spend['Limit'],'Amount']=(50*cust_spend['Limit']).div(100)


# In[33]:


cust_spend[cust_spend['Amount']>cust_spend['Limit']]


# (c) In case repayment amount is more than the limit replace the repayment within limit.

# In[34]:


cust.head(1)


# In[35]:


repay.head(1)


# In[36]:


cust_repay=pd.merge(left=cust,right=repay,how="inner",left_on="Customer",right_on="Customer")


# In[37]:


cust_repay.head(2)


# In[38]:


cust_repay[cust_repay['Amount']>cust_repay['Limit']]


# In[39]:


cust_repay.loc[cust_repay['Amount']>cust_repay['Limit'],'Amount']= cust_repay['Limit']


# In[40]:


cust_repay[cust_repay['Amount']>cust_repay['Limit']]


# 2.(a) How many distinct customers exist?

# In[41]:


cust["Customer"].nunique()


# 2.(b) How many distinct categories exist?

# In[42]:


cust['Segment'].nunique()


# In[43]:


cust['Segment'].value_counts()


# 2.(c) What is the average monthly spend by customers?

# In[44]:


spend.head(2)


# In[45]:


spend.info()


# In[46]:


spend['Month'] = pd.to_datetime(spend['Month'], format='%d-%b-%y')


# In[47]:


repay['Month'] = pd.to_datetime(repay['Month'], format='%d-%b-%y')


# In[48]:


spend.info()


# In[49]:


spend['Monthly'] =spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[50]:


spend.head()


# In[51]:


spend['Monthly'] =spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[52]:


spend['Yearly'] =spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[53]:


spend.head()


# In[54]:


custspends = round(spend.groupby(by=['Yearly','Monthly']).Amount.mean(),2).reset_index()
custspends


# 2.(d)  What is the average monthly repayment by customers?

# In[55]:


repay.info()


# In[56]:


repay['Monthly'] =repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[57]:


repay['Yearly'] =repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[58]:


repay.head(2)


# In[59]:


custrepay = round(repay.groupby(by=['Yearly','Monthly']).Amount.mean().reset_index(),2)
custrepay


# 2.(e) If the monthly rate of interest is 2.9%, what is the profit for the bank for each month? 
# (Profit is defined as interest earned on Monthly Profit. Monthly Profit = Monthly repayment 
# – Monthly spend. Interest is earned only on positive profits and not on negative amounts)

# In[60]:


cust_spend.head()


# In[61]:


repay.head(2)


# In[62]:


customer_final = pd.merge(left=cust_spend , right=repay , on=['Customer'] , how='inner',suffixes=('_spend','_repay'))
customer_final


# In[63]:


Monthly_group = customer_final.groupby(["Yearly", "Monthly"])[['Amount_spend', 'Amount_repay']].sum()
Monthly_group


# In[64]:


Monthly_group['monthly_profit'] = Monthly_group.Amount_repay - Monthly_group.Amount_spend
Monthly_group


# In[65]:


Monthly_group['interst_earned'] = Monthly_group.monthly_profit * 0.029
Monthly_group


# 2.(f) What are the top 5 product types?

# In[66]:


Top_5 =spend.Type.value_counts().head()
Top_5


# In[67]:


Top_5 =spend.Type.value_counts().head().plot(kind='bar')
Top_5


# 2.(g) g. Which city is having maximum spend?
# 

# In[68]:


cust_spend


# In[69]:


spend1 = cust_spend.groupby(by='City').Amount.sum().sort_values(ascending = False)
spend1


# In[70]:


spend1.plot(kind='pie')
plt.title("Amount spent on credit card by customers from different cities")
plt.show()


# 2.(h) Which age group is spending more money?

# In[71]:


cust_spend.Age.min()


# In[72]:


cust_spend.Age.max()


# In[73]:


cust_spend['Age_group'] = pd.cut(cust_spend.Age,5)
cust_spend


# In[74]:


max_cust = cust_spend.groupby(by='Age_group').Amount.sum().sort_values(ascending= False)
max_cust


# In[75]:


max_cust.plot(kind='pie')


# 2.(i) Who are the top 10 customers in terms of repayment?

# In[76]:


cust_Repay = repay.groupby(by='Customer').Amount.sum().sort_values(ascending = False).head(10)
cust_Repay


# In[77]:


cust_Repay.plot(kind='bar')


# 3. Calculate the city wise spend on each product on yearly basis. Also include a graphical 
# representation for the same.
# 

# In[78]:


cust_spend['Month'] = pd.to_datetime(cust_spend['Month'])


# In[79]:


cust_spend['Years'] = cust_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))
cust_spend


# In[80]:


customer_spend_pivot = cust_spend.pivot_table(index=['City','Years'],columns='Product',values= 'Amount',aggfunc='sum')
customer_spend_pivot


# In[81]:


customer_spend_pivot.plot(kind = 'bar',figsize=(13,9))
plt.ylabel('Amount Spend')
plt.title("Bar plot for amount spend City wise on product on Yearly Basis")
plt.show()


# 4.(a)  Monthly comparison of total spends, city wise
# 

# In[82]:


cust_spend['Monthly'] = cust_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[83]:


cust_spend


# In[84]:


city_wise_spend = cust_spend.groupby(by=['Monthly','City']).Amount.sum().sort_index().reset_index()
city_wise_spend


# In[85]:


city_wise_spend = pd.pivot_table(index='City',columns='Monthly',values='Amount',data=cust_spend,aggfunc='sum')
city_wise_spend


# In[86]:


city_wise_spend.plot(kind='bar',figsize=(14,10))
plt.show()


# 4.(b) Comparison of yearly spend on air tickets

# In[87]:


air_tickets = cust_spend.groupby(by=['Years','Type']).Amount.sum().reset_index()
air_tickets.head()


# In[88]:


at = air_tickets[air_tickets.Type == 'AIR TICKET']
at


# In[89]:


at = air_tickets[air_tickets.loc[:,'Type']=='AIR TICKET']
at


# In[90]:


plt.bar(at.Years,height=at.Amount)
plt.xlabel('AIR TICKET')
plt.xlabel('Amount')
plt.title("Comparison of yearly spend on air tickets")
plt.show()


# 4.(c) c. Comparison of monthly spend for each product (look for any seasonality

# In[91]:


prod = cust_spend.pivot_table(index='Product',columns='Monthly',values='Amount',aggfunc='sum')
prod.T


# In[92]:


prod.plot(kind='bar',figsize=(14,9))
plt.xlabel('Product')
plt.ylabel('Amount')
plt.title('Comparison of monthly spend for each product')
plt.show()


# 5.  Write user defined PYTHON function to perform the following analysis:
# You need to find top 10 customers for each city in terms of their repayment amount by 
# different products and by different time periods i.e. year or month. The user should be able 
# to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the 
# function should automatically take these inputs while identifying the top 10 customers.

# In[93]:


cust_repay.head()


# In[94]:


cust_repay.dtypes


# In[95]:


cust_repay['Month']= pd.to_datetime(cust_repay['Month'])


# In[96]:


cust_repay.dtypes


# In[97]:


cust_repay['Monthly'] = cust_repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format='%B'))
cust_repay['Yearly'] =cust_repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[98]:


cust_repay.head()


# In[99]:


cust_repay.groupby(by='Product').Amount.sum()


# In[100]:


cust_repay.groupby(by='City').Amount.sum()


# In[107]:


def summ(Product,timeperiod):
    print("enter the product and timeperiod")
    if Product.lower == 'gold' and timeperiod.lower == 'monthly':
        pivot = cust_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result
    elif Product.lower()=='gold' and timeperiod.lower()=='yearly':
        pivot = cust_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result
    elif Product.lower()=='platimum' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result
    elif Product.lower()=='platimum' and timeperiod.lower()=='monthly':
        pivot = cust_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result
    elif Product.lower()=='silver' and timeperiod.lower()=='monthly':
        pivot = cust_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result
    elif Product.lower()=='silver' and timeperiod.lower()=='yearly':
        pivot = cust_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',values='Amount',aggfunc='sum')
        result = pivot.loc[('Gold',['BANGALORE','BOMBAY','CALCUTTA','CHENNAI','COCHIN','DELHI','PATNA','TRIVANDRUM']),:]
        return result


# In[108]:


summ('silver','yearly')


# In[ ]:





# In[ ]:




