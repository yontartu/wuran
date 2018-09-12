
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import joypy
import seaborn as sns
import datetime

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df08 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2008'
                  ,skiprows=2,encoding='utf-8')
df08.head()


# In[3]:


df08 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2008'
                 ,skiprows=2)
df09 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2009' 
                   , skiprows=2)
df10 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2010' 
                   , skiprows=2)
df11 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2011' 
                   , skiprows=2)
df12 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2012' 
                   , skiprows=2)
df13 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2013' 
                   , skiprows=2)
df14 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2014' 
                   , skiprows=2)
df15 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2015' 
                   , skiprows=3) #different
df16 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2016' 
                   , skiprows=3) #different
df17 = pd.read_csv('/home/bbobjackson/projects/aqi/data/beijing_2017' 
                   , skiprows=3) #different

print(df16.shape)
df16.head()


# In[4]:


#df_comb = df08.append(df09)
df_comb = pd.concat([df08, df09, df10, df11, df12, df13, df14, df15, df16, df17])
print(df_comb.shape)
df_comb.tail()
df_comb = df_comb.reset_index(drop=True)
df_comb.tail()


# #### Compare line countes of original data files using `$ wc -l <filename>` with shape of dataframe
# 
# Each smaller dataframe should have 4 fewer lines, accountings for data descriptions, spacings and headers

# In[5]:


#5087 + 8760*6 + 8784*2 + 4344 #check looks good!
5091 + 8764*6 + 8788*2 + 4348 - 4*10 


# In[6]:


df_comb = df_comb.rename(columns={'Site':'site'
                        ,'Parameter':'parameter'
                        ,'Date (LST)':'dt'
                        ,'Year':'year'
                        ,'Month':'month'
                        ,'Day':'day'
                        ,'Hour':'hour'
                        ,'Value':'value'
                        ,'Duration':'duration'
                        ,'QC Name':'qc_name'})
df_comb['unit'] = 'micrograms per sq meter'
df_comb.head()


# In[7]:


print(df_comb.groupby('qc_name').size())
print('\nPercent values missing: ', round(266.0/4821, 3))


# In[8]:


df_comb.groupby(['qc_name','year']).size()


# ##### Yearly average coming down over time, from a relative peak in 2013

# In[9]:


df_comb[df_comb.qc_name == 'Valid'].groupby('year')['value'].mean().plot(kind='bar')
#df_comb[df_comb.qc_name == 'Valid'].groupby('year')['value'].median()


# ##### Winter months tend to be worse, with December highest

# In[10]:


df_comb[df_comb.qc_name == 'Valid'].groupby('month')['value'].mean().plot(kind='bar')


# ##### Pollution tends to be worse at night, as average levels start to rise starting between 4pm and 5pm and staying elevated until 5am or so

# In[11]:


df_comb[df_comb.qc_name == 'Valid'].groupby('hour')['value'].mean().plot(kind='bar')


# In[12]:


df_comb.groupby(['qc_name','value']).size()
# how to treat valid values that are negative? just code as missing? so filter on 'value' < 0


# In[13]:


def fill_missing(x):
    if x < 0:
        return None
    else:
        return x
    
a = fill_missing(-1)
print(a)


# In[14]:


df_comb[df_comb.qc_name == 'Missing'].value.apply(fill_missing)
df_comb['val'] = df_comb.value.apply(fill_missing)
df_comb[df_comb.qc_name == 'Missing']
df_comb.iloc[694:700] #looks good


# In[15]:


dates = [pd.to_datetime(d) for d in df_comb.dt]
dates[:5]


# In[16]:


y = df_comb.val

plt.figure(figsize=(15,6))
plt.scatter(dates, y, alpha=0.5, s=.1)
plt.show()


# ##### Trying to recreate this graph produced by [Quartz](https://qz.com/197786/six-years-of-bejing-air-pollution-summed-up-in-one-scary-chart/)

# In[17]:


df_comb['dt'] = pd.to_datetime(df_comb.dt)
df_comb.head()


# In[18]:


m = pd.DataFrame({'max_pm25':df_comb.groupby(df_comb.dt.apply(lambda x: x.date()))['val'].max()}).reset_index()
print(m.shape)
m.tail()


# Concentration (ug/m^3) to AQI conversion taken from [AQICN](http://aqicn.org/calculator)

# In[19]:


#0		12		35.5		55.5		150.5		250.5		350.5		500.5
a = m[m.max_pm25 <= 12]
b = m[(m.max_pm25 > 12) & (m.max_pm25 <= 35.5)]
c = m[(m.max_pm25 > 35.5) & (m.max_pm25 <= 55.5)]
d = m[(m.max_pm25 > 55.5) & (m.max_pm25 <= 150.5)]
e = m[(m.max_pm25 > 150.5) & (m.max_pm25 <= 250.5)]
f = m[(m.max_pm25 > 250.5) & (m.max_pm25 <= 350.5)]
g = m[(m.max_pm25 > 350.5) & (m.max_pm25 <= 500.5)]


# In[20]:


days = [pd.to_datetime(date) for date in m.dt]
days[:5]

plt.figure(figsize=(15,6))
plt.scatter(list(a.dt), a.max_pm25, alpha=1.0, s=30, c='g')
plt.scatter(list(b.dt), b.max_pm25, alpha=0.5, s=30, c='y')
plt.scatter(list(c.dt), c.max_pm25, alpha=0.4, s=30, c='orange')
plt.scatter(list(d.dt), d.max_pm25, alpha=0.1, s=30, c='r')
plt.scatter(list(e.dt), e.max_pm25, alpha=0.4, s=30, c='r')
plt.scatter(list(f.dt), f.max_pm25, alpha=0.5, s=30, c='purple')
plt.scatter(list(g.dt), g.max_pm25, alpha=0.5, s=30, c='black')
plt.show()


# In[21]:


sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Create the data
rs = np.random.RandomState(1979)
x = rs.randn(500) #
g = np.tile(list("ABCDEFGHIJ"), 50) #
df = pd.DataFrame(dict(x=x, g=g)) #
m = df.g.map(ord)
df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, size=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color, 
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "x")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play will with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)


# In[22]:


d = df_comb[['year','val']]
d.tail()


# In[28]:


# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(d, row="year", hue="year", aspect=10, size=.7, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "val", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "val", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color, 
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "val")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play will with overlap
g.set_titles("")
g.set(yticks=[])
#g.set(xticks=[])
g.set_xlabels('')
g.set(xlim=[-50,300])
g.despine(bottom=True, left=True)


# ## To Do
# - Code up dates of Party Congresses, Olympics, and other events
# - Convert concentrations to AQI
# - Download data and perform exploratory analysis for Chengdu, Guangzhou, Shanghai and Shenyang 
# - https://en.wikipedia.org/wiki/Air_quality_index#History_of_the_AQI
