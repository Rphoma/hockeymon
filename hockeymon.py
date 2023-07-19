import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import urllib
from PIL import Image
import seaborn as sns
import scipy

pl_white = '#FEFEFE'
pl_background = '#162B50'
pl_text = '#72a3f7'
pl_line_color = '#293a6b'

sns.set_theme(
    style={
        'axes.edgecolor': pl_line_color,
        'axes.facecolor': pl_background,
        'axes.labelcolor': pl_white,
        'xtick.color': pl_white,
        'ytick.color': pl_white,
        'figure.facecolor':pl_background,
        'grid.color': pl_background,
        'grid.linestyle': '-',
        'legend.facecolor':pl_background,
        'text.color': pl_white
     }
    )

# Gen 1
color_scheme = ['#FF5959',
               '#F5AC78',
               '#FAE078',
                '#8EC7BC',
               '#FA92B2']
@st.cache_data
def load_data():
    return pd.read_csv('https://docs.google.com/spreadsheets/d/1pB-ZW1QXPWu8Mdg84WWBanLbl1P95lKWOcQMumhrh0E/export?format=csv&gid=1502323586')
sim_frame = load_data()

# Player
players = list(sim_frame['Player'].unique())
default_ix = players.index('Jason Robertson')
player = st.selectbox('Selct a player:', players, index=default_ix)
# player='Jason Robertson'

# Gen 1
def similarity_card(player=player):
    sim_score = sim_frame.loc[sim_frame['Player']==player,'Sim_Score'].values[0]
    pokemon = sim_frame.loc[sim_frame['Player']==player,'Pokémon'].values[0]
    pokedex_num = sim_frame.loc[sim_frame['Pokémon']==pokemon,'#'].values[0]

    hockey_stats = {'Time On Ice':'TOI_GP',
                    'EV Offense':'xEVO_GAR', 
                    'EV Defense':'xEVD_GAR', 
                    'Spec. Teams':'xST_GAR',
                    'Penalties':'Pens_GAR'}


    poke_stats = ['HP','Attack', 'Defense', 
                  'Special','Speed']

    fig = plt.figure(figsize=(8,10))

    # Parameters to divide card
    grid_height = 3
    grid_width = 6

    # Divide card into tiles
    grid = plt.GridSpec(grid_height, grid_width, 
                        hspace=0, wspace=1.5,
                        height_ratios=[6,6,1])

    ax = plt.subplot(grid[0, :3])
    ax.text(0.4,0.9,f"{player}'s",size=25,va='center',ha='center')
    ax.text(0.4,0.8,f"Most Similar Pokémon:",size=15,va='center',ha='center')
    ax.text(0.4,0.6,f"{pokemon}",size=50,va='center',ha='center')
    ax.text(0.4,0.35,f"Similarity Score:",size=15,va='center',ha='center')
    ax.text(0.4,0.2,f"{sim_score:.0f}/100",size=40,va='center',ha='center')
    ax.axis('off')

    poke_loc = f'https://github.com/Blandalytics/hockeymon/blob/main/poke_pics/{pokedex_num}.png?raw=true'
    poke_pic = Image.open(urllib.request.urlopen(poke_loc))
    ax = plt.subplot(grid[0, 3:])
    ax.imshow(poke_pic)
    ax.axis('off')

    ax = plt.subplot(grid[1, :3])
    sns.barplot(x=list(sim_frame.loc[sim_frame['Player']==player,
                                     ['TOI_GP_scale','xEVO_GAR_scale', 'xEVD_GAR_scale', 
                                      'xST_GAR_scale','Pens_GAR_scale']].values[0]),
                y=list(hockey_stats.keys()),
                palette=color_scheme,
                ax=ax
               )
    for chart_stat in hockey_stats.keys():
        chart_val = sim_frame.loc[sim_frame['Player']==player,hockey_stats[chart_stat]+'_scale'].values[0]
        text_val = sim_frame.loc[sim_frame['Player']==player,hockey_stats[chart_stat]].values[0]
        ax.text(chart_val-0.05 if chart_val>=0.3 else chart_val+0.05,
                list(hockey_stats.keys()).index(chart_stat),
                f'{text_val:.1f}',
                ha='right' if chart_val>=0.3 else 'left',
                va='center',
                color=color_scheme[list(hockey_stats.keys()).index(chart_stat)],
                bbox=dict(facecolor=pl_background, edgecolor=pl_background),
                size=16,
                fontweight='bold')

    ax.set(xlim=(0,1.1))
    ax.get_xaxis().set_visible(False)
    plt.yticks(fontsize=12)
    plt.tick_params(left = False)

    ax = plt.subplot(grid[1, 3:])
    sns.barplot(x=list(sim_frame.loc[sim_frame['Player']==player,
                                    ['HP_scale','Attack_scale','Defense_scale',
                                     'Special_scale','Speed_scale']].values[0]),
                y=['HP','Attack', 'Defense', 
                   'Special','Speed'],
                palette=color_scheme,
                ax=ax
               )
    for chart_stat in poke_stats:
        chart_val = sim_frame.loc[sim_frame['Player']==player,chart_stat+'_scale'].values[0]
        text_val = sim_frame.loc[sim_frame['Player']==player,chart_stat].values[0]
        ax.text(chart_val-0.05 if chart_val>=0.3 else chart_val+0.05,
                poke_stats.index(chart_stat),
                f'{text_val:.0f}',
                ha='right' if chart_val>=0.3 else 'left',
                va='center',
                color=color_scheme[poke_stats.index(chart_stat)],
                bbox=dict(facecolor=pl_background, edgecolor=pl_background),
                size=16,
                fontweight='bold')
    ax.set(xlim=(0,1.1))
    ax.get_xaxis().set_visible(False)
    plt.yticks(fontsize=12)
    plt.tick_params(left = False)

    ax = plt.subplot(grid[2, 0:])
    ax.text(0.4,0.5,f"Based on percentile of Evolving-Hockey's xGAR Metrics\n(Spec. Teams = xPPO + xSHD) and percentile of Pokémon's stats",size=12,va='center',ha='center')
    ax.axis('off')

    sns.despine(bottom=True)
    st.pyplot(fig)

similarity_card()
