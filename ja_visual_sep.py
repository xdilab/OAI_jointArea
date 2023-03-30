import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.colors import to_rgb
from matplotlib.collections import PolyCollection

df = pd.read_csv('data_KL_samples.csv')
df2= pd.read_csv('data_patients.csv')
print(df.head())
print(df.shape)
print(df.loc[((df['inner']<0) | (df['mid']<0) | (df['mid']<0)), ['inner','mid','outer']]) # .mean(axis=0)
df.loc[df['side']=='Left',"side"]= "Left Knee"
df.loc[df['side']=='Right',"side"]= "Right Knee"
df2.loc[df2['side']=='Left',"side"]= "Left Knee"
df2.loc[df2['side']=='Right',"side"]= "Right Knee"
# sea = sns.FacetGrid(df, row="kl", height=1.7, aspect=4)
# sea.map(sns.violinplot, x='kl', y="outer" ,data=df,hue=df['side'])
dic= {"kl":"KL-grade","outer":"Lateral Joint Line (pixel)","inner":"Medial Joint Line (pixel)","mid":"Center Joint Line (pixel)","side":"Side", 'left':"Left Knee",'right':"Right Knee"}
df=df.rename(columns=dic)
df2=df2.rename(columns=dic)
kl, outer, inner, mid, side, left, right = dic['kl'], dic['outer'], dic['inner'], dic['mid'], dic['side'], dic['left'],dic['right']
split=True
print(df.head())

rgb1 = to_rgb('lime') # 0.5 + 0.5 * np.array(to_rgb('dodgerblue'))
rgb2 = to_rgb('cyan') # 0.5 + 0.5 * np.array(to_rgb('crimson'))
palette = [to_rgb("blue"),to_rgb("crimson"),to_rgb("green"),to_rgb("black"),to_rgb("orange")]

# TODO: lateral ########
fig, axes = plt.subplots(1, 1)
fig.set_figheight(3.5) # 3.7
fig.set_figwidth(6)
size_marker =  None
p = sns.violinplot(ax=axes,x=kl, y=outer ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes,x=4.9, y=outer ,data=df2.loc[df2['Side']==left], hue='color', palette=palette,size=size_marker  )
sns.scatterplot(ax=axes,x=5.1, y=outer ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker  )
# axes.legend(loc='lower left')
# axes.get_legend().remove()
x = [0,1,2,3,4,5]
my_xticks= ["0","1", "2", "3", "4", "Patients (L|R)"]
plt.xticks(x, my_xticks)
stepsize = 30
# plt.yticks(np.arange(min(outer), max(outer)+1, 10.0))
start, end = p.get_ylim()
p.yaxis.set_ticks(np.arange(start, end, stepsize))
axes.plot([5, 5], [0, 1750], color='black',linewidth=1) # , marker = ''
# plt.subplots_adjust(wspace=0, hspace=0)
# plt.legend('', frameon=False)
#Fix legend
# plt.legend('', frameon=False)
for ax in [axes]:
    hand, labl = ax.get_legend_handles_labels()
    handout=[]
    lablout=[]
    for h,l in zip(hand,labl):
       if l not in lablout:
            lablout.append(l)
            handout.append(h)
    ax.legend(handout, lablout, loc='upper center', bbox_to_anchor=(0.5, 1.27), # (0.51, 1.01) (0.555, 0.97)
          ncol=4, fancybox=False, shadow=False)
# axes.get_legend().remove()
# plt.legend('', frameon=False)
plt.show()
plt.tight_layout()
# plt.legend('', frameon=False)
# plt.savefig('svg_lateral.svg')
# plt.clf()

# TODO: medial ########

fig, axes = plt.subplots(1, 1)
fig.set_figheight(3.5)
fig.set_figwidth(6)
size_marker =  None

p=sns.violinplot(ax=axes,x=kl, y=inner ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes,x=4.9, y=inner ,data=df2.loc[(df2['Side']==left)], hue='color', palette=palette ,size=size_marker  )
sns.scatterplot(ax=axes,x=5.1, y=inner ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker  )
# axes.legend(loc='lower left')
# axes[1].get_legend().remove()
x = [0,1,2,3,4,5]
my_xticks= ["0","1", "2", "3", "4", "Patients (L|R)"]
plt.xticks(x, my_xticks)
# plt.yticks(np.arange(min(outer), max(outer)+1, 10.0))
start, end = p.get_ylim()
p.yaxis.set_ticks(np.arange(start, end, stepsize))
axes.plot([5, 5], [0, 1500], color='black',linewidth=1)
# plt.subplots_adjust(wspace=0, hspace=0)

# plt.legend('', frameon=False)
#Fix legend
for ax in [axes]:
    hand, labl = ax.get_legend_handles_labels()
    handout=[]
    lablout=[]
    for h,l in zip(hand,labl):
       if l not in lablout:
            lablout.append(l)
            handout.append(h)
    ax.legend(handout, lablout, loc='upper center', bbox_to_anchor=(0.5, 1.27),
          ncol=4, fancybox=False, shadow=False)

plt.show()
plt.tight_layout()
# plt.savefig('svg_medial.svg')
# plt.clf()

# TODO: center ########

fig, axes = plt.subplots(1, 1)
fig.set_figheight(3.5)
fig.set_figwidth(6)
size_marker =  None

p=sns.violinplot(ax=axes,x=kl, y=mid ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box' ,cut=0) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes,x=4.9, y=mid ,data=df2.loc[df2['Side']==left], hue='color', palette=palette,size=size_marker  )
sns.scatterplot(ax=axes,x=5.1, y=mid ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker   ) #, palette=palette [rgb2]*5
# axes.legend(loc='lower left')
x = [0,1,2,3,4,5]
my_xticks= ["0","1", "2", "3", "4", "Patients (L|R)"]
plt.xticks(x, my_xticks)
# plt.yticks(np.arange(min(outer), max(outer)+1, 10.0))
start, end = p.get_ylim()
p.yaxis.set_ticks(np.arange(start, end, stepsize))
axes.plot([5, 5], [0, 1500], color='black',linewidth=1)
# plt.subplots_adjust(wspace=0, hspace=0)

# plt.legend('', frameon=False)
#Fix legend
for ax in [axes]:
    hand, labl = ax.get_legend_handles_labels()
    handout=[]
    lablout=[]
    for h,l in zip(hand,labl):
       if l not in lablout:
            lablout.append(l)
            handout.append(h)
    ax.legend(handout, lablout, loc='upper center', bbox_to_anchor=(0.5, 1.27),
          ncol=4, fancybox=False, shadow=False)
# plt.subplots_adjust(wspace=0, hspace=0)

plt.show()
plt.tight_layout()
# plt.savefig('svg_center.svg')
# plt.clf()

