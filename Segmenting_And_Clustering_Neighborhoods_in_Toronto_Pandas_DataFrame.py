
# coding: utf-8

# ### Installing all the required applications

# In[152]:


get_ipython().system('conda install -c conda-forge geopy --yes')
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')

print ('Geopy installed')
print ('Folium installed')


# ### Importing all the required packages

# In[153]:


import requests # library to handle requests 
import pandas as pd 
import numpy as np
import random


from geopy.geocoders import Nominatim

#libaries for displaying images 
from IPython.display import Image 
from IPython.core.display import HTML

#transforming json file into a pandas dataframe library
from pandas.io.json import json_normalize


import folium
import lxml.html as lh


# ### URL for the Wikipedia page containing Toronto Neighbourhood data

# In[154]:


url     = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
url


# ### Extracting the contents of the URL

# In[155]:


page = requests.get(url)
print (page.text)


# ### Storing the contents as doc parameter

# In[156]:


#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
[len(T) for T in tr_elements[:12]]


# ### Extracting the table containing the Toronto Neighbourhoods from the URL content

# In[157]:


tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    #print '%d:"%s"'%(i,name)
    col.append((name,[]))

for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[158]:


[len(C) for (title,C) in col]


# ### Creating a dataframe 'df' from the table extracted 

# In[159]:


Dict={title:column for (title,column) in col }
df=pd.DataFrame(Dict)
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
df = df.replace('\n','', regex=True)
df.head()


# In[160]:


df.columns


# ### Removing the newline character from the 'Neighbourhood' column

# In[161]:


df.rename(columns={'Neighbourhood\n':'Neighbourhood'}, inplace=True)
df.columns


# ### Assigning Borough name to Neighbourhood if value of Neighbourhood = 'Not Assigned'

# In[162]:


df.Neighbourhood[df.Neighbourhood == 'Not assigned'] = df.Borough
df.head()


# ### Extracting the Boroughs which are Not equal to 'Not Assigned'

# In[163]:


df_filtered = df[df['Borough'] != 'Not assigned']
df_filtered.head()


# ### Grouping Neighbourhood for the same Postcode and Borough

# In[166]:


df_Toranto = df_filtered.groupby(['Postcode','Borough'])['Neighbourhood'].apply(','.join).reset_index()
df_Toranto


# ### Finding the shape of the Toronto Neighbourhood dataframe

# In[167]:



df_Toranto.shape

