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

fig, axes = plt.subplots(3, 1)
fig.set_figheight(9)
fig.set_figwidth(6)
size_marker =  None

sns.violinplot(ax=axes[0],x=kl, y=outer ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes[0],x=4.9, y=outer ,data=df2.loc[df2['Side']==left], hue='color', palette=palette,size=size_marker  )
sns.scatterplot(ax=axes[0],x=5.1, y=outer ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker  )
axes[0].legend(loc='lower left')
axes[0].get_legend().remove()
axes[0].plot([5, 5], [0, 1750], color='black',linewidth=1) # , marker = ''
# extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# fig.savefig('avg_left.png', bbox_inches=extent)

sns.violinplot(ax=axes[2],x=kl, y=inner ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes[2],x=4.9, y=inner ,data=df2.loc[(df2['Side']==left)], hue='color', palette=palette ,size=size_marker  )
sns.scatterplot(ax=axes[2],x=5.1, y=inner ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker  )
axes[2].legend(loc='lower left')
axes[2].get_legend().remove()
axes[2].plot([5, 5], [0, 1500], color='black',linewidth=1)
# extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# fig.savefig('ax2_figure.png', bbox_inches=extent)

sns.violinplot(ax=axes[1],x=kl, y=mid ,data=df,hue=side, hue_order=[left,right], palette=[rgb1, rgb2], split=split, inner='box' ,cut=0) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
sns.scatterplot(ax=axes[1],x=4.9, y=mid ,data=df2.loc[df2['Side']==left], hue='color', palette=palette,size=size_marker  )
sns.scatterplot(ax=axes[1],x=5.1, y=mid ,data=df2.loc[df2['Side']==right], hue='color', palette=palette,size=size_marker   ) #, palette=palette [rgb2]*5
axes[1].legend(loc='lower left')
axes[1].get_legend().remove()
x = [0,1,2,3,4,5]
my_xticks= ["0","1", "2", "3", "4", "Patients (L|R)"]
plt.xticks(x, my_xticks)
axes[1].plot([5, 5], [0, 1500], color='black',linewidth=1)
# extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# fig.savefig('ax2_figure.png', bbox_inches=extent)

# for ax in axes:
#     x1, y1 = [5.1, 5.1], [0, 1500]
#     # x2, y2 = [1, 10], [3, 2]
#     ax.plot(x1, y1, color='black') # , marker = ''

plt.legend('', frameon=False)
#Fix legend
for ax in [axes[2]]:
    hand, labl = ax.get_legend_handles_labels()
    handout=[]
    lablout=[]
    for h,l in zip(hand,labl):
       if l not in lablout:
            lablout.append(l)
            handout.append(h)
    fig.legend(handout, lablout, loc='upper center', bbox_to_anchor=(0.51, 0.945),
          ncol=4, fancybox=False, shadow=False)


print(df2[(df2['Side']==left)].shape)
print(df2[(df2['Side']==right)].shape)
print(df2[(df2['Side']==left)].head(10))
print(df2[(df2['Side']==right)].head(10))
print(to_rgb("blue"),to_rgb("crimson"),to_rgb("green"),to_rgb("black"),to_rgb("orange"))
# fig, axes = plt.subplots(3, 1)
# sns.boxplot(ax=axes[0],x=kl, y=outer ,data=df,hue=side, hue_order=["Left","Right"], palette=[rgb1, rgb2] ) # , split=split,inner='stick', inner='box',cut=0 #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
# axes[0].legend(loc='lower left')
# axes[0].get_legend().remove()
# sns.violinplot(ax=axes[1],x=kl, y=inner ,data=df,hue=side, hue_order=["Left","Right"], palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
# sns.swarmplot(ax=axes[1],x=kl, y=inner ,data=df,hue=side, hue_order=["Left","Right"], palette=[rgb1, rgb2] ) # , split=split
# axes[1].legend(loc='lower left')
# axes[1].get_legend().remove()
# sns.swarmplot(ax=axes[2],x=kl, y=mid ,data=df,hue=side, hue_order=["Left","Right"], palette=[rgb1, rgb2]) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
# axes[2].legend(loc='lower left')

# fig, axes = plt.subplots(3, 1)
# # Create violin plots without mini-boxplots inside.
# axes[0] = sns.violinplot(ax=axes[0],x=kl, y=outer ,data=df, palette=[rgb1, rgb2], split=split, inner='box',cut=0)
# # Clip the right half of each violin.
# for item in axes[0].collections:
#     x0, y0, width, height = item.get_paths()[0].get_extents().bounds
#     item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
#                        transform=axes[0].transData))
# # Create strip plots with partially transparent points of different colors depending on the group.
# num_items = len(axes[0].collections)
# sns.stripplot(ax=axes[0],x=kl, y=outer ,data=df, palette=[rgb1, rgb2], alpha=0.4, size=7)
# # Shift each strip plot strictly below the correponding volin.
# for item in axes[0].collections[num_items:]:
#     item.set_offsets(item.get_offsets() + 0.15)
# # Create narrow boxplots on top of the corresponding violin and strip plots, with thick lines, the mean values, without the outliers.
# sns.boxplot(ax=axes[0],x=kl, y=outer ,data=df, palette=[rgb1, rgb2], width=0.25,
#             showfliers=False, showmeans=True,
#             meanprops=dict(marker='o', markerfacecolor='darkorange',
#                            markersize=10, zorder=3),
#             boxprops=dict(facecolor=(0,0,0,0),
#                           linewidth=3, zorder=3),
#             whiskerprops=dict(linewidth=3),
#             capprops=dict(linewidth=3),
#             medianprops=dict(linewidth=3))
# axes[0].legend(loc='lower left')
# axes[0].get_legend().remove()
# sns.violinplot(ax=axes[1],x=kl, y=inner ,data=df, palette=[rgb1, rgb2], split=split, inner='box',cut=0  ) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
# axes[1].legend(loc='lower left')
# axes[1].get_legend().remove()
# sns.violinplot(ax=axes[2],x=kl, y=mid ,data=df, palette=[rgb1, rgb2], split=split, inner='box' ,cut=0) #.set(title='Outer Joint Space in Pixels') # [df['kl']==4] # ['side']].apply(tuple, axis=1)
# axes[2].legend(loc='lower left')



# plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
# plt.show()
# move axes

plt.savefig('svg_all.svg')

# df_stack = pd.DataFrame()
# kl = 4
# side = 'Left'
# print(df.loc[(df['kl']==kl) & (df['side']==side), ['inner','mid','outer']].mean(axis=0)) #

