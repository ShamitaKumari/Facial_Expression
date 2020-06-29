#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:01:19 2020

@author: shamita
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import seaborn as sns
import random
df=pd.read_excel('F_Expression.xlsx')
oasis_df=pd.read_csv('OASIS_ImageSet.csv')
oasis=['Theme','Valence_mean','Valence_SD']
new_oasis=oasis_df[oasis]
#change column name Theme into Stimulus Name in oasis dataset
new_oasis = new_oasis.rename(columns={'Theme': 'Stimulus Name','Valence_mean':'OASIS_Valence_mean',
                                      'Valence_SD':'OASIS_Valence_SD'})
new_oasis1 = new_oasis.rename(columns={'Theme': 'Stimulus Name','Valence_mean':'OASIS_Valence_mean',
                                      'Valence_SD':'OASIS_Valence_SD'})
# =============================================================================
# drop all the unnecessary columns & row for a more refined data
# =============================================================================
#drop all the blankblnk from stimulus Name 
ind_drop = df[df['Stimulus Name'].apply(lambda x: x.startswith('BlankBlk'))].index
new_df = df.drop(ind_drop)
#drop Breath and Hands from dataset as they are not important
ind_drop = new_df[df['Stimulus Name'].apply(lambda x: x.startswith('Breathe'))].index
new_df1 = new_df.drop(ind_drop)
ind_drop = new_df1[df['Stimulus Name'].apply(lambda x: x.startswith('Hands'))].index
new_df2 = new_df1.drop(ind_drop)
#Drop unneceassary columns such as Threshold
new_df2.columns=new_df2.columns.str.replace(r' >= Threshold$','')
#replacing ' <= Threshold$' with emty space
new_df2.columns=new_df2.columns.str.replace(r' <= Threshold$','')
#try to drop columns with contain "Threshold"
#creating an array column names which doesn't contains "Threshold"
column_names = [ x for x in new_df2.head(0) if "Threshold" not in x ]
#modifing the dataframe with remaining column names
df1=new_df2[column_names]
#creating another dataframe with specific columns
df2=['Stimulus Name','Age','Positive Time Percent','Positive Count Frames','Negative Count Frames',
     'Negative Time Percent']
print(df2)
#drop 0 values and calculate mean and std of Positive time percent
new = df1[df2]

# =============================================================================
# Drop all 0 values which are considered as noise.
# =============================================================================
#drop all the 0 values from Positive and Negative time Percent columns
NewPositive= new[new['Positive Time Percent'] !=0 ]
NewNegitive =  new[new['Negative Time Percent'] !=0 ]
#drop 0 values of Positive & Negative time percent (copy for Mapped Scores)
NewPositive1= new[new['Positive Time Percent'] !=0 ]
NewNegitive1 =  new[new['Negative Time Percent'] !=0 ]


# =============================================================================
# Distribution Graphs for Positive and Negative Column Before and After Mapping
# =============================================================================

#sns.distplot(new['Positive Time Percent'],norm_hist= True,rug=True, kde=True, hist=False)
#sns.distplot(new['Negative Time Percent'],norm_hist= True,rug=True, kde=True, hist=False)

#distribution before mapping
sns.distplot(NewPositive['Positive Time Percent'],  rug=True, kde=True, hist=False)
#distribution after mapping
sns.distplot(NewPositive1['Positive Time Percent'],rug=True, kde=True, hist=False)

#distribution before mapping (Negative time Percent)
sns.distplot(NewNegitive['Negative Time Percent'],rug=True, kde=True, hist=False)
#distribution before mapping (Negative time Percent)
sns.distplot(NewNegitive1['Negative Time Percent'],rug=True, kde=True, hist=False)



# =============================================================================
# Mapping the scores of Positive and Negative Time Percent for level matching
# =============================================================================

#mapping of positiv andNegative Time Percent
NewNegitive1.loc[(NewNegitive1['Negative Time Percent']>=23.19) & (NewNegitive1['Negative Time Percent']<34.88),'Negative Time Percent']=-3
NewNegitive1.loc[(NewNegitive1['Negative Time Percent']>=11.6) & (NewNegitive1['Negative Time Percent']<23.19),'Negative Time Percent']=-2
NewNegitive1.loc[(NewNegitive1['Negative Time Percent']>=0.01) & (NewNegitive1['Negative Time Percent']<11.6),'Negative Time Percent']=-1
NewPositive1.loc[(NewPositive1['Positive Time Percent']>=0)  &(NewPositive1['Positive Time Percent']<0.1),'Positive Time Percent']=0
NewPositive1.loc[(NewPositive1['Positive Time Percent']>=0.1) & (NewPositive1['Positive Time Percent']<33.33),'Positive Time Percent']=1
NewPositive1.loc[(NewPositive1['Positive Time Percent']>=33.33) & (NewPositive1['Positive Time Percent']<66.67),'Positive Time Percent']=2
NewPositive1.loc[(NewPositive1['Positive Time Percent']>=66.67) & (NewPositive1['Positive Time Percent']<100),'Positive Time Percent']=3

NewPositive1.loc[(NewPositive1['Negative Time Percent']>=0.01) & (NewPositive1['Negative Time Percent']<11.6),'Negative Time Percent']=-1
NewPositive1.loc[(NewPositive1['Negative Time Percent']>=11.6) & (NewPositive1['Negative Time Percent']<23.19),'Negative Time Percent']=-2
NewNegitive1.loc[(NewNegitive1['Positive Time Percent']>=0.1) & (NewNegitive1['Positive Time Percent']<33.33),'Positive Time Percent']=1
NewNegitive1.loc[(NewNegitive1['Positive Time Percent']>=33.33) & (NewNegitive1['Positive Time Percent']<66.67),'Positive Time Percent']= 2

#concat positive and Negative time percent into new dataset
Data_Merge= pd.concat([NewPositive,NewNegitive], sort=False)
Data_Merge1=['Stimulus Name','Positive Time Percent','Negative Time Percent']
Data_Merge=Data_Merge[Data_Merge1]
#concat positive and Negative time percent into new dataset (after mapping dataset)
Data_Mapping= pd.concat([NewPositive1,NewNegitive1], sort=False)
Data_Merge2=['Stimulus Name','Positive Time Percent','Negative Time Percent']
Data_Mapping=Data_Mapping[Data_Merge2]
# =============================================================================
#                         ####Another way of mapping the Column scores####
# =============================================================================

# ##divide the values by 28.57 to match the level of Scores (-3 to 3).
# ##We are dividing it by 28.57 because we assume total of both (positive and Negative value ) columns is 200. (200/7=28.57)
# #New_Positive= Data_Merge['Positive Time Percent']/28.57
# #New_Negitive= Data_Merge['Negative Time Percent']/28.57
# ##divide the values by 14.285 to match the level of Scores (-3 to 3). 
# ##We are dividing it by 14.285 because positive and negative scores lies between 0-100. (100/7=14.285)
# #New_Positive= Data_Merge['Positive Time Percent']/14.285
# #New_Negitive= Data_Merge['Negative Time Percent']/14.285
# #adding columns into Data_Merge Dataframe
# #Data_Merge['New_Positive']=New_Positive
# #Data_Merge['New_Negitive']=New_Negitive
# #convert Negative Column into negative values for plotting on Y- Negative
# #Data_Merge.New_Negitive=Data_Merge.New_Negitive*(-1)
# =============================================================================


# =============================================================================
# Mean and SD of iMotion columns Before and After Mapping
# =============================================================================

# Mean and SD for Positive Time Percent before Mapping
iMotions_Positive_mean=Data_Merge.groupby('Stimulus Name')['Positive Time Percent'].mean()
iMotions_Positive_std=Data_Merge.groupby('Stimulus Name')['Positive Time Percent'].std(ddof=0)
# Mean and SD for Positive Time Percent (Mapped Columns)
iMotions_Positive_Mean=Data_Mapping.groupby('Stimulus Name')['Positive Time Percent'].mean()
iMotions_Positive_Std=Data_Mapping.groupby('Stimulus Name')['Positive Time Percent'].std(ddof=0)

# Mean and SD for Negative Time Percent Before Mapping
iMotions_Negitive_mean=Data_Merge.groupby('Stimulus Name')['Negative Time Percent'].mean()
iMotions_Negitive_std=Data_Merge.groupby('Stimulus Name')['Negative Time Percent'].std(ddof=0)
# Mean and SD for Negative Time Percent after Mapping
iMotions_Negitive_Mean=Data_Mapping.groupby('Stimulus Name')['Negative Time Percent'].mean()
iMotions_Negitive_Std=Data_Mapping.groupby('Stimulus Name')['Negative Time Percent'].std(ddof=0)



#Create new DF MeanDFrame
p_N_data_dict={'iMotions_Positive_mean':iMotions_Positive_mean,'iMotions_Negitive_mean':iMotions_Negitive_mean,
               'iMotions_Positive_std':iMotions_Positive_std,'iMotions_Negitive_std':iMotions_Negitive_std}
Mean_DFrame=pd.DataFrame(p_N_data_dict).reset_index()
Mean_DFrame.columns=['Stimulus Name','iMotions_Positive_mean','iMotions_Negitive_mean',
                     'iMotions_Positive_std','iMotions_Negitive_std']
print(Mean_DFrame)


#Create new DF MeanDFrame for Mapped values
p_N_data_dict1={'iMotions_Positive_Mean':iMotions_Positive_Mean,'iMotions_Negitive_Mean':iMotions_Negitive_Mean,
               'iMotions_Positive_Std':iMotions_Positive_Std,'iMotions_Negitive_Std':iMotions_Negitive_Std}
Mean_DFrame1=pd.DataFrame(p_N_data_dict1).reset_index()
Mean_DFrame1.columns=['Stimulus Name','iMotions_Positive_Mean','iMotions_Negitive_Mean',
                     'iMotions_Positive_Std','iMotions_Negitive_Std']
print(Mean_DFrame1)

# =============================================================================
# #Individual visualization of Error Bars for iMotions Columns and Oasis 
# =============================================================================
# #visualization of IMotion data ( Mean of Positive Time Percent with error Bars)
CTe1=(Mean_DFrame.iMotions_Positive_mean)
error=(Mean_DFrame.iMotions_Positive_std)
materials = (Mean_DFrame['Stimulus Name'])
x_pos1 = np.arange(len(materials))
 
fig, ax = plt.subplots()
ax.bar(x_pos1, CTe1, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('values')
ax.set_xticks(x_pos1)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and Std of Positive time Percent Before Mapping')
ax.yaxis.grid(True)

# #visualization of IMotion data After Mapping ( Mean of Positive Time Percent with error Bars)
CTe1=(Mean_DFrame1.iMotions_Positive_Mean)
error=(Mean_DFrame1.iMotions_Positive_Std)
materials = (Mean_DFrame1['Stimulus Name'])
x_pos1 = np.arange(len(materials))
 
fig, ax = plt.subplots()
ax.bar(x_pos1, CTe1, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('values')
ax.set_xticks(x_pos1)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and Std of Positive time Percent After Mapping')
ax.yaxis.grid(True)


# #visualization of IMotion data ( Mean of Negative Time Percent with error Bars)
CTe1=(Mean_DFrame.iMotions_Negitive_mean)
error=(Mean_DFrame.iMotions_Negitive_std)
materials = (Mean_DFrame['Stimulus Name'])
x_pos1 = np.arange(len(materials))
 
fig, ax = plt.subplots()
ax.bar(x_pos1, CTe1, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('values')
ax.set_xticks(x_pos1)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and Std of Negative time Percent Before Mapping Before Mapping')
ax.yaxis.grid(True)


# #visualization of IMotion data After Mapping ( Mean of Negative Time Percent with error Bars)
CTe1=(Mean_DFrame1.iMotions_Negitive_Mean)
error=(Mean_DFrame1.iMotions_Negitive_Std)
materials = (Mean_DFrame1['Stimulus Name'])
x_pos1 = np.arange(len(materials))
 
fig, ax = plt.subplots()
ax.bar(x_pos1, CTe1, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('values')
ax.set_xticks(x_pos1)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and Std of Negative time Percent After Mapping')
ax.yaxis.grid(True)

# =============================================================================
# Oasis Mapping score for level matching
# =============================================================================

#Oasis Mapping
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=0) & (new_oasis1['OASIS_Valence_mean']<1),'OASIS_Valence_mean']=-3
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=1) & (new_oasis1['OASIS_Valence_mean']<2),'OASIS_Valence_mean']=-2
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=2) & (new_oasis1['OASIS_Valence_mean']<3),'OASIS_Valence_mean']=-1
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=3)  &(new_oasis1['OASIS_Valence_mean']<4),'OASIS_Valence_mean']= 0
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=4) & (new_oasis1['OASIS_Valence_mean']<5),'OASIS_Valence_mean']= 1
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=5) & (new_oasis1['OASIS_Valence_mean']<6),'OASIS_Valence_mean']= 2
new_oasis1.loc[(new_oasis1['OASIS_Valence_mean']>=6) & (new_oasis1['OASIS_Valence_mean']<7),'OASIS_Valence_mean']= 3

#Merge Oasis and iMotions Data
iMo_Oasis=pd.merge(new_oasis,Mean_DFrame,how='inner', on=['Stimulus Name'])
#Merge Oasis and iMotions Data For mapped Scores
iMo_Oasis1=pd.merge(new_oasis1,Mean_DFrame1,how='inner', on=['Stimulus Name'])


#Oasis valence and SD bar graph with Error Bars
CTe=(iMo_Oasis.OASIS_Valence_mean)
error=(iMo_Oasis.OASIS_Valence_SD)
materials = (iMo_Oasis['Stimulus Name'])
x_pos = np.arange(len(materials))

fig, ax = plt.subplots()
ax.bar(x_pos, CTe, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=8)
ax.set_ylabel('values')
ax.set_xticks(x_pos)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and error of Oasis values Before mapping')
ax.yaxis.grid(True)

#Oasis valence and SD bar graph with Error Bars
CTe=(iMo_Oasis1.OASIS_Valence_mean)
error=(iMo_Oasis1.OASIS_Valence_SD)
materials = (iMo_Oasis1['Stimulus Name'])
x_pos = np.arange(len(materials))

fig, ax = plt.subplots()
ax.bar(x_pos, CTe, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=8)
ax.set_ylabel('values')
ax.set_xticks(x_pos)
ax.set_xticklabels(materials, rotation=90)
ax.set_title('Mean and error of Oasis values Before mapping')
ax.yaxis.grid(True)


#plot iMotions and Oasis Error Bar on Y positive and Negative axis After mapping
fig, ax = plt.subplots()
ax=iMo_Oasis1.plot.bar(x='Stimulus Name', 
                 y=['iMotions_Positive_Mean','iMotions_Negitive_Mean','OASIS_Valence_mean'],
                 yerr=iMo_Oasis1[['iMotions_Positive_Std','iMotions_Negitive_Std','OASIS_Valence_SD']].T.values,capsize=6,
                 align='center', ecolor='black',figsize=(8,7),
                 title='iMotion Comparison error Bar of Positive nd Negative with Oasis After Mapping')
ax.grid(axis='y')
plt.tight_layout()
plt.savefig('1st approach for Neg/Pos together bar.png')
plt.show()



#Bar Graph with  mean values of Positive and Negative along with OASIS AFTER MAPPING
fig, ax = plt.subplots()
graph=pd.DataFrame(iMo_Oasis1, columns=['Stimulus Name','OASIS_Valence_mean','iMotions_Positive_Mean','iMotions_Negitive_Mean' ])

graphCompare=graph.groupby('Stimulus Name')
graphComparisonPlot= graphCompare.sum().plot(kind='bar',
                                     title='Comparison Bar of iMotions individual column mean values with Oasis After Mapping ',
                                     figsize=(8,6),
                                     align='center', capsize=10,ax=ax)
ax.grid(axis='y')
plt.savefig('1st Approach with subtraction.png')

# =============================================================================
#                                   2Nd Approach 
#(Combined Mean of Positive and Negative columns as iMotions Mean and comparison with Oasis)
# =============================================================================

#2nd Approach
#MEAN AFTER ADDITION OF SERIES
#convert Negative Column into negative values for plotting on Y- Negative
#Data_Merge.New_Negitive=Data_Merge.New_Negitive*(-1)
#Adding mean values of positive and Negative Columns 
# ===========================================================================================================
# Additon of Positive and Negative Coulmns and then calculate the combined Mean and SD (results are similar)
# ================================================================================================================
#new1 = df1[df2]
#addition = new1['Positive Time Percent']+new1['Negative Time Percent']
#new1['addition']=addition
#SumOfPosNeg_Mean = new1.groupby('Stimulus Name')['addition'].mean() 
#SumOfPosNeg_std=new1.groupby('Stimulus Name')['addition'].std() 
#iMo_Oasis1['SumOfPosNeg_Mean']=SumOfPosNeg_Mean
#iMo_Oasis1['SumOfPosNeg_std']=SumOfPosNeg_std
#print(SumOfPosNeg_Mean)
#print(SumOfPosNeg_std)

#Adding mean values of positive and Negative Columns  AFTER MAPPING
iMotions_Mean =Mean_DFrame1['iMotions_Positive_Mean']+Mean_DFrame1['iMotions_Negitive_Mean']
Mean_DFrame1['iMotions_Mean']=iMotions_Mean
iMotions_Std =Mean_DFrame1['iMotions_Positive_Std']+Mean_DFrame1['iMotions_Negitive_Std']
Mean_DFrame1['iMotions_Std']=iMotions_Std
iMo_Oasis1['iMotions_Mean']=iMotions_Mean
iMo_Oasis1['iMotions_Std']=iMotions_Std


#Visualize comparios Error bar of iMotions and Oasis After Mapping
fig, ax = plt.subplots()
ax=iMo_Oasis1.plot.bar(x='Stimulus Name', 
                 y=['iMotions_Mean','OASIS_Valence_mean'],
                 yerr=iMo_Oasis1[['iMotions_Std','OASIS_Valence_SD']].T.values,capsize=6,
                 align='center', ecolor='black',figsize=(8,7), 
                 title='iMotion Comparison error Bar of Positive nd Negative with Oasis'),
ax.grid(axis='y')
plt.tight_layout()
plt.savefig('2nd approach for Neg/Pos together bar.png')
plt.show()

#comparison graph of iMotions and Oasis AFTER MAPPING

fig, ax = plt.subplots()
graph=pd.DataFrame(iMo_Oasis1, columns=['Stimulus Name','OASIS_Valence_mean','iMotions_Mean'])
graphCompare=graph.groupby('Stimulus Name')
graphComparisonPlot= graphCompare.sum().plot(kind='bar',
                                     title='Comparison of iMotions Mean values with Oasis After Mapping  ',
                                     figsize=(8,6),align='center', capsize=10,ax=ax)
ax.grid(axis='y')
plt.savefig('2nd Approach with subtraction.png')


# =============================================================================
#                                 ###COUNT FRAME###
# =============================================================================#                                        
#                                          
##drop all the 0 values from Positive and Negative time Percent columns
#PosCountFrame= new[new['Positive Count Frames'] !=0 ]
#NegCountFrame =  new[new['Negative Count Frames'] !=0 ]
#
##concat positive and Negative time percent into new dataset
#CF_Data_Merge= pd.concat([PosCountFrame,NegCountFrame], sort=False)
#CF_Data_Merge1=['Stimulus Name','Positive Count Frames','Negative Count Frames']
#CF_Data_Merge=CF_Data_Merge[CF_Data_Merge1]
#
###divide the values by 28.57 to match the level of Scores (-3 to 3).
###We are dividing it by 28.57 because we assume total of both (positive and Negative value ) columns is 200. (200/7=28.57)
#New_CF_Positive= CF_Data_Merge['Positive Count Frames']/28.57
#New_CF_Negitive= CF_Data_Merge['Negative Count Frames']/28.57
#
###divide the values by 14.285 to match the level of Scores (-3 to 3). 
###We are dividing it by 14.285 because positive and negative scores lies between 0-100. (100/7=14.285)
##New_Positive= Data_Merge['Positive Time Percent']/14.285
##New_Negitive= Data_Merge['Negative Time Percent']/14.285
##adding columns into Data_Merge Dataframe
#CF_Data_Merge['New_CF_Positive']=New_CF_Positive
#CF_Data_Merge['New_CF_Negitive']=New_CF_Negitive  
#
##convert Negative Column into negative values for plotting on Y- Negative
#CF_Data_Merge.New_CF_Negitive=CF_Data_Merge.New_CF_Negitive*(-1)
#
## Mean and SD for Positiveive Time Percent
#iMotions_CF_Positive_mean=CF_Data_Merge.groupby('Stimulus Name')['New_CF_Positive'].mean()
#iMotions_CF_Positive_std=CF_Data_Merge.groupby('Stimulus Name')['New_CF_Positive'].std()
#
## Mean and SD for Negative Time Percent
#iMotions_CF_Negitive_mean=CF_Data_Merge.groupby('Stimulus Name')['New_CF_Negitive'].mean()
#iMotions_CF_Negitive_std=CF_Data_Merge.groupby('Stimulus Name')['New_CF_Negitive'].std()
#
#
#
##Create new DF MeanDFrame
#p_N_data_dict1={'iMotions_CF_Positive_mean':iMotions_CF_Positive_mean,'iMotions_CF_Negitive_mean':iMotions_CF_Negitive_mean,
#               'iMotions_CF_Positive_std':iMotions_CF_Positive_std,'iMotions_CF_Negitive_std':iMotions_CF_Negitive_std}
#Mean_CF_DFrame=pd.DataFrame(p_N_data_dict1).reset_index()
#Mean_CF_DFrame.columns=['Stimulus Name','iMotions_CF_Positive_mean','iMotions_CF_Negitive_mean',
#                     'iMotions_CF_Positive_std','iMotions_CF_Negitive_std']
#print(Mean_CF_DFrame)
#
#
##turn Oasis Valence column from -3 to 3 range
#Oasis_ValenceMean=new_oasis['OASIS_Valence_mean']-4
#new_oasis['Oasis_ValenceMean']=Oasis_ValenceMean
#iMo_Oasis1=pd.merge(new_oasis,Mean_CF_DFrame,how='inner', on=['Stimulus Name'])
#
# 
#                        
##plot iMotions Count Frame and Oasis Error Bar on Y positive and Negative axis
#fig, ax = plt.subplots()
#ax=iMo_Oasis1.plot.bar(x='Stimulus Name', 
#                 y=['iMotions_CF_Positive_mean','iMotions_CF_Negitive_mean','Oasis_ValenceMean'],
#                 yerr=iMo_Oasis1[['iMotions_CF_Positive_std','iMotions_CF_Negitive_std','OASIS_Valence_SD']].T.values,capsize=6,
#                 align='center', ecolor='black',figsize=(8,7), 
#                 title='iMotion Comparison error Bar of Positive nd Negative with Oasis')
#ax.grid(axis='y')
#plt.tight_layout()
#plt.savefig('1st approach for Neg/Pos together bar.png')
#plt.show()
#
#
##Bar Graph with seprate mean values of Positive and Negative Count Frame along with OASIS
#fig, ax = plt.subplots()
#graph=pd.DataFrame(iMo_Oasis1, columns=['Stimulus Name','iMotions_CF_Positive_mean','iMotions_CF_Negitive_mean',
#                                           'Oasis_ValenceMean'])
#graphCompare=graph.groupby('Stimulus Name')
#graphComparisonPlot= graphCompare.sum().plot(kind='bar',
#                                     title='Comparison Bar of iMotions individual column mean values with Oasis  ',figsize=(8,6),
#                                     align='center', capsize=10,ax=ax, color=['red', 'orange', 'lightgreen', 'darkgreen'])
#ax.grid(axis='y')
#plt.savefig('1st Approach with subtraction.png')
                  
