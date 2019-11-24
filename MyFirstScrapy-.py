
# coding: utf-8

# # Make more money by buying lottery? 
# ## --- (Python Crawler+Data Analysis)

# ## Introduction
# 
# **In this report, I will extract 100 pages of '3d' lottery data from http://www.zhcw.com to see if there is any strategy to make more money by buying the lottery. '3d' lottery is one of the favorite lottery game in China. People can choose 3 numbers from 000 to 999 and wait for one winning numbers. Firstly, let's see the data structure: we have Date(One time per day), period, winning numbers, sale amount and reward ratio.**

# ![jupyter](./data.jpeg)

# ## Get the Data
# 
# **By analyzing the web source code, and using the 'Requests' package, 'Xpath' method to get the lottery data from 2013 to current date.**

# In[1]:


import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'} #Simulate the browser, keep-alive to make the process 
url = 'http://kaijiang.zhcw.com/zhcw/html/3d/list_1.html'
response = requests.get(url = url,headers = headers)
print(response)


# **Code '200' means that the we can successfully extract the data.**

# In[2]:


response_default = requests.get(url = url)
print(response_default.request.headers)


# **The code is not always equal 200 because some website did not allow the python to extract the information. Thus, we need change our heaeders sometimes to make the website always know that it is not the robot(python) to extract the data.**

# In[3]:


response.request.headers


# In[4]:


from lxml import etree


# In[5]:


res_xpath = etree.HTML(response.text) #turn html to xpath structure


# In[6]:


print(res_xpath.xpath('/html/body/table//tr[3]/td[2]/text()'))


# In[7]:


trs = res_xpath.xpath('/html/body/table//tr')


# **trs will have 20 elements to be stored because there are 20 items shown in one page.**

# In[8]:


print(trs)


# ## Write the data into Excel

# In[9]:


import xlwt


# In[10]:


#create one working sheet
f = xlwt.Workbook()


# In[11]:


lotto = f.add_sheet('lottery',cell_overwrite_ok=True)


# In[12]:


#header in excel
row = ['Date','Period','number1','number2','number3','sale_amount','reward ratio']
for i in range(0,len(row)):
    lotto.write(0,i,row[i])


# In[ ]:


#We need to scrap more data so we need different url and same process above.(I plan to get 100 pages of lottery info)
#we have already opened a xls file and have it headers.


# In[13]:


j = 1
for i in range(1,101):
    url = 'http://kaijiang.zhcw.com/zhcw/html/3d/list_{}.html'.format(i)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    response = requests.get(url = url,headers = headers)
    res_xpath = etree.HTML(response.text)
    trs = res_xpath.xpath('/html/body/table//tr')
    
    for tr in trs[2:-1]:
        lotto.write(j,0,tr.xpath('./td[1]/text()'))
        lotto.write(j,1,tr.xpath('./td[2]/text()'))
        lotto.write(j,2,tr.xpath('./td[3]/em[1]/text()'))
        lotto.write(j,3,tr.xpath('./td[3]/em[2]/text()'))
        lotto.write(j,4,tr.xpath('./td[3]/em[3]/text()'))
        lotto.write(j,5,tr.xpath('./td[7]/strong[1]/text()'))
        lotto.write(j,6,tr.xpath('./td[8]/text()'))
        j += 1


# In[14]:


f.save('lotto.xls')


# **Now,we have our xls file to store 2000 lottery data (2000 days)**

# ## Analyze the data

# In[15]:


import pandas as pd


# In[16]:


data = pd.read_csv('lotto.csv')


# In[17]:


data.head()


# In[18]:


data.info() #there is no missing value to be imputed


# In[19]:


#visualization
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# **from the data, the there is no significant correlation between winning numbers and orders.**

# In[20]:


figsize = 18,4
fig = plt.figure(figsize=figsize)
ax1 = fig.add_subplot(1,3,1)
ax1.hist(data['number1'])
ax1.set_title('number1')
ax2 = fig.add_subplot(1,3,2)
ax2.hist(data['number2'],color='green')
ax2.set_title('number2')
ax3 = fig.add_subplot(1,3,3)
ax3.hist(data['number3'],color='pink')
ax3.set_title('number3')


# **Next I will examine whether the company will prefer any specific number**

# In[21]:


li1 = []
for i in range(2,5):
    for j in data.iloc[:,i]:
        li1.append(j)


# In[22]:


#plt.hist(li1,orientation='horizontal')
for i in range(10):
    print('number',i,':',li1.count(i))


# **it seems number 3 7 8 is more likely to be chosen, next I will find the relationship between numbers and date.**

# In[23]:


li2 = []
for i in range(0,2000):
    li2.append(pd.to_datetime(data.iloc[i,0]).weekday()+1)


# In[24]:


data['DayoftheWeek'] = li2


# In[25]:


data.head() #1:Monday,2:Thuesday..7:Sunday


# In[26]:


data[data['DayoftheWeek']==1].head()


# In[27]:


#set the function to count each number in every day of the week
def countday(data):
    li1 = []
    for i in range(2,5):
        for j in data.iloc[:,i]:
            li1.append(j)
    for i in range(10):
        print('number',i,':',li1.count(i),' probability:',round(li1.count(i)/len(li1),3))      


# In[28]:


countday(data[data['DayoftheWeek']==1])


# ## Conclusion
# 
# **After checking every date, I make a table for chossing the best 3 numbers for each day of the week, which is the most likely numbers in that day based on these 5 years dataset. However, this strategy may not the best one to use, and we need combine more data to consider. We cannot use lottery to earn money even we have better strategy because, actually, each number will have eventually same probability (1/10) to be picked, and we should just have fun playing it.**

# In[29]:


from prettytable import PrettyTable
x= PrettyTable(["Day of Week", "number1", 'number2','number3'])
x.add_row(['Monday',7,8,9])
x.add_row(["Thuesday",4,6,8])
x.add_row(["Wednesday",3,5,8])
x.add_row(["Thursday",1,3,8])
x.add_row(["Friday",3,6,8])
x.add_row(["Saturday",1,7,0])
x.add_row(["Sunday",1,0,7])
print(x)

