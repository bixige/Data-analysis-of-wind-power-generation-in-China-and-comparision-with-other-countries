#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
color = sns.color_palette()
sns.set_style('white')
import warnings
warnings.filterwarnings('ignore')


# **<font size=5>Read thermal, hydro, wind, solar and nuclear production data into dataframe</font>**

# In[2]:


df1 = pd.read_csv('/Users/KUANGBixi/Downloads/UNdata_Export_Electricity - total thermal production.csv')
df2 = pd.read_csv('/Users/KUANGBixi/Downloads/UNdata_Export_Electricity - total hydro production.csv')
df3 = pd.read_csv('/Users/KUANGBixi/Downloads/UNdata_Export_Electricity - total wind production.csv')
df4 = pd.read_csv('/Users/KUANGBixi/Downloads/UNdata_Export_Electricity - total solar production.csv')
df5 = pd.read_csv('/Users/KUANGBixi/Downloads/UNdata_Export_Electricity - total nuclear production.csv')
df = df1.append([df2, df3, df4, df5], ignore_index=True)


# In[3]:


df.head()


# **<font size=5>Realize the basic information about the data</font>**

# In[4]:


df.columns = ['country','commodity','year','unit','quantity','footnotes']
df.tail()


# In[5]:


df.isnull().sum()


# In[6]:


df.describe(include=['object'])


# In[7]:


df.country.value_counts().head()


# In[8]:


df.commodity.value_counts().head()


# **<font size=5>Determine top 6 countries wind power production</font>**

# In[9]:


commodity_string = 'Electricity - total wind production'
df_wind = df[df.commodity.str.contains
                  (commodity_string)]
df_max = df_wind.groupby(pd.Grouper(key='country'))['quantity'].max()
df_max = df_max.sort_values(ascending=False)
df_max = df_max[:6]


# In[10]:


df_max = df[df.commodity.str.contains
            (commodity_string)].groupby(pd.Grouper(key='country'))['quantity'].max().sort_values(ascending=False)[:6]
range = np.arange(2000,2018)
dict_major = {}
for c in df_max.index.values:
    read_index = df_wind[df_wind.commodity.str.contains(commodity_string) & df_wind.country.str.contains(c + '$')].year
    read_data = df_wind[df_wind.commodity.str.contains(commodity_string) & df_wind.country.str.contains(c + '$')].quantity
    read_data.index=read_index
    prod = read_data.reindex(index=range,fill_value=0)
    dict_major.update({c:prod.values})
df_major = pd.DataFrame(dict_major)
df_major.index = range
df_major


# **<font size=5>Plot bar graphic to present the growth of wind Power Production for major countries</font>**

# In[11]:


ax = df_major.plot(kind='bar', stacked=False,figsize=(20,10))
plt.title('Wind energy production')
plt.xlabel('Year')
plt.ylabel("Millions of Kilowatts-Hour")


# **<font size=5>Plot bar graphic to describe the growth of wind Power Production in China after 2007</font>**

# In[12]:


ax = df_major['China'].plot(kind='bar', stacked=False,figsize=(20,10))
plt.title('Wind energy production of China')
plt.xlabel('Year')
plt.ylabel("Millions of Kilowatts-Hour")


# **<font size=5>Plot line graphic to describe the growth of wind Power Production for major countries</font>**

# In[13]:


df_max


# In[14]:


CHI = df[df.country.str.contains('China')].sort_values('year')
US = df[df.country.str.contains('United States')].sort_values('year')
GER = df[df.country.str.contains('Germany')].sort_values('year')
SP = df[df.country.str.contains('Spain')].sort_values('year')
BR= df[df.country.str.contains('Brazil')].sort_values('year')
UK = df[df.country.str.contains('United Kingdom')].sort_values('year')


# In[15]:


CHI_Wind = CHI[CHI.commodity == 'Electricity - total wind production'].sort_values('year')
US_Wind = US[US.commodity == 'Electricity - total wind production'].sort_values('year')
GER_Wind = GER[GER.commodity == 'Electricity - total wind production'].sort_values('year')
SP_Wind = SP[SP.commodity == 'Electricity - total wind production'].sort_values('year')
BR_Wind = BR[BR.commodity == 'Electricity - total wind production'].sort_values('year')
UK_Wind = UK[UK.commodity == 'Electricity - total wind production'].sort_values('year')


# In[16]:


GER_Wind.country = 'Germany'


# In[17]:


y1 = CHI_Wind.quantity
x1 = CHI_Wind.year
y2 = US_Wind.quantity
x2 = US_Wind.year
y3 = GER_Wind.quantity
x3 = GER_Wind.year
x4 = SP_Wind.year
y4 = SP_Wind.quantity
x5 = BR_Wind.year
y5 = BR_Wind.quantity
x6 = UK_Wind.year
y6 = UK_Wind.quantity


# In[18]:


plt.figure(figsize=(15,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.plot(x1,y1,'b',linestyle='dashed', marker='o',
         markersize=12, label='China')
plt.plot(x2,y2,'r',linestyle='dashed', marker='D',
         markersize=12, label="US")
plt.plot(x3,y3,'y',linestyle='dashed', marker='>',
         markersize=12,label="Germany")
plt.plot(x4,y4,'k',linestyle='dashed', marker='2',
         markersize=12,label="Spain")
plt.plot(x5,y5,'g',linestyle='dashed', marker='*',
         markersize=12,label="Brazil")
plt.plot(x6,y6,'c',linestyle='dashed', marker='d',
         markersize=12,label="UK")

plt.legend(fontsize=16)
plt.ylabel("Millions of Kilowatts-Hour",fontsize=20)
plt.xlabel('Year',fontsize=20)
plt.title('Total Wind production of top6 countries after 2000',fontsize=24)
plt.xlim(2000, 2017)
plt.show()


# **<font size=5>Utilize plotly to plot wind Power Production in different countries on world map</font>**

# In[19]:


df_wind_top6 = CHI_Wind.append([CHI_Wind, US_Wind, GER_Wind, SP_Wind, BR_Wind, UK_Wind], ignore_index=True)
df_wind_top6.tail()


# In[20]:


code = {'Brazil': 'BRA',
 'China': 'CHN',
 'Germany': 'DEU',
 'Spain': 'ESP',
 'United Kingdom': 'GBR',
 'United States': 'USA'}


# In[21]:


df_code = pd.DataFrame(df_wind_top6.country.transform(lambda x: code[x]))
df_wind_top6['code'] = df_code
df_wind_top6


# In[22]:


df_wind_top6_2016 = df_wind_top6[df_wind_top6.year == 2016].sort_values(ascending=False,by='quantity')[:]
df_wind_top6_2016


# In[23]:


df_wind_top6_2016.drop(index=[8], inplace=True)
df_wind_top6_2016


# **<font size=5>Plot wind Power Production in top 6 countries for 2016 on world map</font>**

# In[24]:


# this code based on example code at: https://plot.ly/python/choropleth-maps/
import plotly.graph_objects as go

fig = go.Figure(data=go.Choropleth(
    locations = df_wind_top6_2016['code'],
    z = df_wind_top6_2016['quantity'],
    text = df_wind_top6_2016['country'],
    colorscale = 'Greens',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Wind Power<br>Millions of Kilowatts-Hour',
))

fig.update_layout(
    title_text='2016 Wind Power Production Top6',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
        showarrow = False
    )]
)

fig.show()


# **<font size=5>Compare Main Power Generation Types in China</font>**

# In[25]:


CHI_thermal = CHI[CHI.commodity == 'Electricity - total thermal production'].sort_values('year')
CHI_hydro = CHI[CHI.commodity == 'Electricity - total hydro production'].sort_values('year')
CHI_nuclear = CHI[CHI.commodity == 'Electricity - total nuclear production'].sort_values('year')
CHI_solar = CHI[CHI.commodity == 'Electricity - total solar production'].sort_values('year')


# In[26]:


CHI_thermal.head()


# In[27]:


CHI_thermal = CHI_thermal[~ CHI_thermal['country'].str.contains('SAR')]
CHI_thermal.head()


# In[28]:


print(CHI_thermal.shape)
print(CHI_hydro.shape)
print(CHI_nuclear.shape)
print(CHI_solar.shape)
print(CHI_Wind.shape)


# **<font size=5>Wind vs. Thermal production</font>**

# In[29]:


bar_width =.7
plt.figure(figsize=(20,10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.bar(CHI_thermal['year'], CHI_thermal['quantity'],bar_width, color='r',capstyle= 'projecting', label='CHI Thermal Production', alpha=0.5)
plt.bar(CHI_Wind['year'], CHI_Wind['quantity'],bar_width, color='b', label='CHI Wind Production', alpha=0.6)

plt.legend(fontsize=16)
plt.xlabel('Years', fontsize=20)
plt.ylabel('Millions of Kilowatts-Hour', fontsize=20)
plt.title('Total Thermal and Wind production in the China', fontsize=24)
plt.xticks(CHI_thermal['year'])
plt.show()


# **<font size=5>Main Types of Clearner Energy (Hydro, Wind, Solar) Comparision in China</font>**

# In[30]:


bar_width =.6
plt.figure(figsize=(20,10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)

plt.bar(CHI_hydro['year'], CHI_hydro['quantity'],bar_width - .1, color='y', label='CHI Solar Production', alpha=0.5)
plt.bar(CHI_Wind['year'], CHI_Wind['quantity'],bar_width, color='b', label='CHI Solar Production', alpha=0.5)
plt.bar(CHI_solar['year'], CHI_solar['quantity'],bar_width, color='m', label='CHI Nuclear Production', alpha=0.5)

plt.legend(fontsize=16)
plt.xlabel('Years', fontsize=20)
plt.ylabel('Millions of Kilowatts-Hour', fontsize=20)
plt.title('Total Hydro, Wind and Solar production (Clearner Energy) in China', fontsize=24)
plt.xticks(CHI_thermal['year'])
plt.show()


# **<font size=5>Top 4 Power Generation Types in China</font>**

# In[31]:


bar_height =0.5
plt.figure(figsize=(15,10))
plt.barh(CHI_thermal['year'], CHI_thermal['quantity'], height = bar_height, color='r', label='CHI Thermal Production')
plt.barh(CHI_hydro['year'], CHI_hydro['quantity'], align ='edge', height=bar_height-.1, color='y', label='CHI Hydro Production')
plt.barh(CHI_nuclear['year'], CHI_nuclear['quantity'], align ='edge', height=bar_height-.2, color='g', label='CHI Nuclear Production')
plt.barh(CHI_Wind['year'], CHI_Wind['quantity'], align ='edge', height=bar_height-.3, color='b', label='CHI Wind Production')


plt.yticks(CHI_thermal['year'])
plt.legend(fontsize=16)
plt.ylabel('Years', fontsize=14)
plt.xlabel('Quantity', fontsize=14)
plt.title('Total Wind, Hydro, Nuclear, and Thermal production in the China', fontsize=24)
plt.xlim()
plt.show()


# In[ ]:




