
# coding: utf-8

# # Project: Investigating BMI
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>
# 
# <a id='intro'></a>
# ## Introduction
# 
# > **Tip**: In this section of the report, provide a brief introduction to the dataset you've selected for analysis. At the end of this section, describe the questions that you plan on exploring over the course of the report. Try to build your report around the analysis of at least one dependent variable and three independent variables. If you're not sure what questions to ask, then make sure you familiarize yourself with the dataset, its variables and the dataset context for ideas of what to explore.
# 
# > If you haven't yet selected and downloaded your data, make sure you do that first before coming back here. In order to work with the data in this workspace, you also need to upload it to the workspace. To do so, click on the jupyter icon in the upper left to be taken back to the workspace directory. There should be an 'Upload' button in the upper right that will let you add your data file(s) to the workspace. You can then click on the .ipynb file name to come back here.

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.

df_bmi_male = pd.read_excel('Indicator_BMI male ASM.xlsx')
df_bmi_female = pd.read_excel('Indicator_BMI female ASM.xlsx')


# In[4]:


# 199 countries, 29 years of BMI data from 1980 - 2008

df_bmi_male.info()
df_bmi_female.info()


# In[5]:


df_bmi_male.describe()


# In[6]:


df_bmi_female.describe()


# In[7]:


# Combining the 2 graphs into one to make it easier to manipulate

bmi_male = np.repeat('male', 199)
bmi_female = np.repeat('female', 199)
df_bmi_male['gender'] = bmi_male
df_bmi_female['gender'] = bmi_female
df_bmi = df_bmi_male.append(df_bmi_female)
df_bmi.head(10)


# ## Some exploration of BMI data

# In[8]:


# Plotting the trend across ~3 decades

df_bmi.loc[df_bmi['gender'] == 'male'].mean().plot(kind='line', color='blue', label = 'male')
df_bmi.loc[df_bmi['gender'] == 'female'].mean().plot(kind='line', color='red', label = 'female')
plt.legend()
plt.title('Mean BMI across 3 decades')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# #### Observations
# 
# 1. Mean BMI has steadily risen globally. 
# 2. Gap between men and women has also been increasing.
# 3. Rate of increase seems to have turned slightly steeper for both men and women between 1995 - 2000.

# In[9]:


# Which segments had the biggest rise in BMI?

df_bmi.columns = df_bmi.columns.astype(str)
df_bmi['bmi_change']= df_bmi['2008'] - df_bmi['1980']
df_bmi_change = df_bmi[['Country', 'gender', 'bmi_change']]
df_bmi_change.set_index('Country').sort_values(by=['bmi_change'], ascending=False).head(20)


# #### Observations
# 
# 1. Segments with the biggest increases in BMI tend to come from the populations in the Pacific Islands. 
# 2. Segments with the biggest increases are typically female.

# In[32]:


# What is the current distribution of countries according to mean BMI levels

ax = df_bmi['2008'].hist()
ax.set_ylabel('No. of Countries')
ax.set_xlabel('Mean BMI')
ax.set_title('Distribution of countries (BMI)')
print('median    {}'.format(df_bmi['2008'].median()))
print(df_bmi['2008'].describe());


# #### Observations
# 
# 1. Graph is close to symmetric
# 2. ~ 50% of the world can be considered overweight/obese

# ## Exploring correlations between BMI and other macro indicators
# 
# Comparisons will be made across 3 other sets of data - working hours, sugar consumption, blood pressure. The first 2 are seen as possible factors that could contribute to growing obesity phenomenon and the last is seen as something that obesity could lead to. 
# 
# Comparisons are done across 2 clusters of countries that are deemed to be similar economically, culturally and perhaps even genetically to enhance perspective.Hypothesis is that data of countries in a cluster will display similar trends.

# ### BMI general trends

# In[10]:


# Plotting trend of mean BMI for first cluster of countries across same time period

df_bmi = df_bmi.iloc[:, 0:30]
df_bmi.loc[df_bmi['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_bmi.loc[df_bmi['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_bmi.loc[df_bmi['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean BMI across ~3 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# #### Observations
# 
# 1. BMI has steadily increased for all three countries at similar rates.
# 2. US has the highest BMI.
# 3. Australia's BMI overtook the UK somewhere between 2000 and 2005.

# In[11]:


# Plotting trend of mean BMI for second cluster of countries across same time period

df_bmi.loc[df_bmi['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_bmi.loc[df_bmi['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_bmi.loc[df_bmi['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean BMI across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# #### Observations
# 
# 1. While BMI for all countries have been increasing steadily, Norway has seen the biggest increase amongst the three.
# 2. Rate of increase in Norway increased around 1995, for Denmark around 1990.

# ### (1) Is there a correlation between working hours and BMI?
# 
# Broad idea here is that societies with long working hours generate unhealthy environments that are not conducive for engaging in dietary habits and other activities (such as exercising) that could ameliorate obesity.

# In[12]:


# Loading data

df_working_hours = pd.read_excel('indicator_hours per week.xlsx')


# In[13]:


# Checking data

df_working_hours.info()


# In[14]:


# Cleaning data to help in comparison efforts

df_working_hours.rename(columns={'Working hours per week': 'Country'}, inplace=True)
df_working_hours.head()


# In[15]:


# Plotting trend of mean number of working hours for first cluster of countries

df_working_hours.loc[df_working_hours['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_working_hours.loc[df_working_hours['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_working_hours.loc[df_working_hours['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean working hours across ~3 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean working hours')
plt.xlabel('Year');


# #### Observations
# 
# 1. Albeit with fluctuations, working hours has generally declined, especially for Australia and the UK.
# 2. Number of working hours peaked just before 1990.
# 3. Rate of decline increased sharply around 2000.
# 4. United States has the highest number of working hours.

# In[16]:


# Plotting trend of mean BMI for first cluster of countries across same time period

df_bmi = df_bmi.iloc[:, 0:30]
df_bmi.loc[df_bmi['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_bmi.loc[df_bmi['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_bmi.loc[df_bmi['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean BMI across ~3 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# The question I had going in was whether or not higher working hours contributed to a higher BMI.
# 
# On the face of it, that does not seem to be the case. The trends are in fact opposite. Any correlation is not clear either. The nature of movement seem very different (i.e. the fluctuations seen in the data on working hours do not correspond with the steady increase in BMI).

# In[17]:


# Plotting trend of mean number of working hours for second cluster of countries

df_working_hours.loc[df_working_hours['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_working_hours.loc[df_working_hours['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_working_hours.loc[df_working_hours['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean working hours across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean working hours')
plt.xlabel('Year');


# #### Observations
# 
# 1. Both Norway and Denmark have seen a decrease in number of working hours, the drop in Norway has been greater.
# 2. Sweden has seen a general increase. 
# 3. Where the data ends post-2005, the Swedish and Danish work for a similar duration across the week.

# In[18]:


# Plotting trend of mean BMI for second cluster of countries across same time period

df_bmi.loc[df_bmi['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_bmi.loc[df_bmi['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_bmi.loc[df_bmi['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean BMI across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# Unlike the previous comparison, where the British had the lowest average working hours and a lower average BMI, and the Americans who had the highest average working hours and the highest BMI, the opposite is observable with regards to Scandinavian countries. The Norwegians generally worked lesser hours in recent years but had the highest BMI, whereas the Danish and Swedes worked more hours but had a lower BMI.
# 
# Also, one could make an observation that a decrease in working hours correlates with an increase in BMI over the same time period, this interestingly does not apply to the Swedish.
# 
# From these 2 comparisons, it is not obvious that there is a discernible and direct relationship between working hours and BMI. It is likely that the BMI of a nation is influenced by several other variables such as their eating habits.

# ### (2) Is there a correlation between sugar consumption and BMI?
# 
# The idea here is simply that there is a direct correlation between sugar consumption and BMI. An increase in the former would correspond with a similar and proportionate increase in the latter.

# In[19]:


# Loading data

df_sugar_consumption = pd.read_excel('indicator sugar_consumption.xlsx')

# Preparing data

df_sugar_consumption.reset_index(inplace=True)
df_sugar_consumption.head()
df_sugar_consumption.rename(columns={'index':'Country'}, inplace=True)
df_sugar_consumption.columns = df_sugar_consumption.columns.astype(str)
df_sugar_consumption = df_sugar_consumption.iloc[:, np.r_[0, 20:45]]
df_sugar_consumption.head()


# In[20]:


# Plotting trend of mean level of sugar consumption for first cluster of countries

df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean sugar consumption across 2.5 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean sugar consumption')
plt.xlabel('Year');


# #### Observations
# 
# 1. Aus and UK saw a decline in sugar consumption, US saw an increase.
# 2. Whatever the trend for the respective countries, sugar consumption starts to plateau around the year 2000.

# In[21]:


# Plotting trend of mean BMI for first cluster of countries across same time period

df_bmi.columns = df_bmi.columns.astype(str)
df_bmi_sc = df_bmi.loc[:, 'Country':'2004']
df_bmi_sc.loc[df_bmi['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_bmi_sc.loc[df_bmi['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_bmi_sc.loc[df_bmi['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean BMI across 3 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# The expected direct correlation does not really play out in this set of data. Aus and UK's mean BMI continues to increase even as their sugar consumption levels go south. Also, the widening gap in sugar consumption between the US on the one hand and Aus and UK does not really manifest itself in the BMI graph.

# In[22]:


# Plotting trend of mean level of sugar consumption for second cluster of countries

df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_sugar_consumption.loc[df_sugar_consumption['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean sugar consumption across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean sugar consumption')
plt.xlabel('Year');


# #### Observations
# 
# 1. All countries saw an increase, but the rate of increase seen in Denmark is significantly higher than Sweden and Norway.

# In[23]:


df_bmi_sc.loc[df_bmi['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_bmi_sc.loc[df_bmi['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_bmi_sc.loc[df_bmi['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean BMI across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# Even though Denmark started as the country with the highest level of sugar consumption and saw the highest increase, their mean BMI remained the lowest (although it does look that their BMI would overtake Sweden in another 5 years). Gap in mean BMI between Norway and Denmark widens with Norway at the front even though sugar consumption data of both countries widens in the opposite direction.
# 
# Sweden's moderate consumption of sugar seems to correspond with their slight increase in BMI over the years.
# 
# One again, echoing the observation made when looking at data from working hours, BMI looks like a complex unit with a range of variables that influence it.

# ### (3) Is there a correlation between BMI and SBP?
# 
# Having looked at some factors that could have played a part in driving BMI, I wanted to investigate BMI as a driving factor. The idea here is simply that there is a direct correlation between BMI and SBP. An increase in the former would correspond with a similar increase in the latter. The data here is broken down between genders mainly due to availability.

# In[24]:


# Loading data

df_sbp_male = pd.read_excel('Indicator_SBP male ASM.xlsx')
df_sbp_female = pd.read_excel('Indicator_SBP female ASM.xlsx')


# In[25]:


# Preparing data

df_sbp_male.rename(columns={'SBP male (mm Hg), age standardized mean':'Country'}, inplace=True)
df_sbp_female.rename(columns={'SBP female (mm Hg), age standardized mean':'Country'}, inplace=True)


# In[27]:


# Plotting trend of mean level of SBP for males in the first cluster of countries

df_sbp_male.loc[df_sbp_male['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_sbp_male.loc[df_sbp_male['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_sbp_male.loc[df_sbp_male['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean SBP across 2.5 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean SBP')
plt.xlabel('Year');


# #### Observations
# 
# 1. General decline in SBP for all three countries.
# 2. UK has the highest SBP, US has the lowest.
# 3. Gap has widened between countries, with US showing the fastest rate of decrease (albeit tapering off)

# In[37]:


# Plotting trend of mean level of BMI for males in the first cluster of countries

df_bmi_male.loc[df_bmi_male['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_bmi_male.loc[df_sbp_male['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_bmi_male.loc[df_sbp_male['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean BMI across 2.5 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# Interestingly, SBP has been on a general decline despite an increase in BMI. Also, while US has the highest BMI, it has the lowest SBP. On the other hand, UK has the lowest BMI but the highest SBP. 

# In[38]:


# Plotting trend of mean level of SBP for females in the first cluster of countries

df_sbp_female.loc[df_sbp_female['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_sbp_female.loc[df_sbp_female['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_sbp_female.loc[df_sbp_female['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean SBP across 2.5 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean SBP')
plt.xlabel('Year');


# #### Observations
# 
# 1. Females on average have lower SBP levels than men.
# 2. Same general declining trend observed as with males.
# 3. SBP for Australian females see significant decrease (seems to have begun in between 1990 - 1995)

# In[39]:


# Plotting trend of mean level of BMI for females in the first cluster of countries

df_bmi_female.loc[df_bmi_female['Country'] == 'Australia'].mean().plot(kind='line', color='blue', label='Aus')
df_bmi_female.loc[df_sbp_female['Country'] == 'United States'].mean().plot(kind='line', color='green', label='US')
df_bmi_female.loc[df_sbp_female['Country'] == 'United Kingdom'].mean().plot(kind='line', color='red', label='UK')
plt.legend()
plt.title('Mean BMI across 2.5 decades (Anglo-Saxon Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# Even though BMI has increased at a faster rate for Australian women than British women, SBP has fallen faster for women in AUS than in the UK.
# 
# On the face of this data, it would seem the correlation between BMI and SBP is the opposite of what was expected. Let's have a look at a second cluster of countries.

# In[44]:


# Plotting trend of mean level of SBP for males in the second cluster of countries

df_sbp_male.loc[df_sbp_male['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_sbp_male.loc[df_sbp_male['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_sbp_male.loc[df_sbp_male['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean SBP across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean SBP')
plt.xlabel('Year');


# #### Observations
# 
# 1. Mean SBP levels of men decrease in a similar fashion.
# 2. Rate of decrease is particularly high pre-1985. Slows down after.
# 3. Norway has the highest levels of SBP, Denmark the lowest.

# In[42]:


# Plotting trend of mean level of BMI for males in the second cluster of countries

df_bmi_male.loc[df_bmi_male['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_bmi_male.loc[df_bmi_male['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_bmi_male.loc[df_bmi_male['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean BMI across 2.5 decades (Scandinavian Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# BMI does not increase in a similar fashion for these 3 countries. BMI increases at a higher rate in Norway and Denmark than Sweden. If trend continues, Sweden would have the lowest BMI out of the 3 countries. Rate of BMI increase also heightens post-1990, particularly for Denmark and Norway.

# In[45]:


# Plotting trend of mean level of SBP for females in the second cluster of countries

df_sbp_female.loc[df_sbp_female['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_sbp_female.loc[df_sbp_female['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_sbp_female.loc[df_sbp_female['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean SBP across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean SBP')
plt.xlabel('Year');


# #### Observations
# 
# 1. Mean SBP levels of women also decrease in a similar fashion.
# 2. Rate of decrease is generally quite uniform across the years.
# 3. Mirroring data from men, Norway has the highest levels of SBP for women, Denmark the lowest.

# In[46]:


# Plotting trend of mean level of BMI for females in the second cluster of countries

df_bmi_female.loc[df_bmi_female['Country'] == 'Norway'].mean().plot(kind='line', color='red', label='Nor')
df_bmi_female.loc[df_bmi_female['Country'] == 'Sweden'].mean().plot(kind='line', color='blue', label='Swe')
df_bmi_female.loc[df_bmi_female['Country'] == 'Denmark'].mean().plot(kind='line', color='orange', label='Den')
plt.legend()
plt.title('Mean BMI across 3 decades (Scandinavian Countries)')
plt.ylabel('Mean BMI')
plt.xlabel('Year');


# Similar to comparison done with men data, BMI does not increase in a similar fashion here. Mean Swedish female BMI increases at a much lower rate as compared to Norway and Denmark.
# 
# This data is surprising in that it is contrary to mainstream scientific expositions that basically link a higher BMI with higher blood pressure. It is however probably unwise to draw any conclusions from this simple comparison. Other factors could very well play crucial roles. For e.g. the decrease in blood pressure could have been a result of higher governmental expenditure on healthcare facilities and breakthroughs in this area of medicine that help contain and lower blood pressure.
# 
# More questions could also be asked about how the data was obtained to determine reliability of data. Better data segmentation factoring in other variables such as age and existing medical conditions could also enhance understanding.

# <a id='conclusions'></a>
# ## Conclusions
# 
# This exploration left me with more questions than answers, with all my initial hypotheses overturned. The data showed me that
# 
# 1. Correlations between BMI and other variables that one would have assumed to be straightforward, was not.
# 2. Countries that I clustered together did not always exhibit similar trends which begs the question why.
# 3. Probably also implies that no single comparison can have a universal conclusion across countries. Each country has its own complex context that influences how one variable affects another. For e.g. in the US higher number of working hours corresponds with higher BMI while in Norway lower number of wokring hours corresponds with higher BMI.
# 
# ### Some things I would have done to improve this report
# 
# 1. When comparing BMI with other variables, instead of looking at them in 2 charts, I would look at them in one more comprehensive line chart with mean BMI levels as a third axis.
# 
# 2. I would have compared a few more variables such as governmental healthcare expenditure to get a fuller picture.
# 
# 3. I would also look at cluster of countries in Asia and Africa to get a more holistic global view.
# 
# > To export the report to the workspace, you should run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the jupyter icon in the upper left). Alternatively, you can download the html report via the **File** > **Download as** submenu and then manually upload it to the workspace directory. Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right. Congratulations!

# In[1]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

