import streamlit as st
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import urllib
from PIL import Image
# import seaborn as sns
# import scipy
# import time

logo = Image.open(urllib.request.urlopen('https://github.com/Blandalytics/hockeymon/blob/main/hockeymon%20logo.png?raw=true'))
st.image(logo)

generations = ['Gen1','Gen2']
poke_gen = st.radio('Choose a generation of Pokémon:', generations)

# pl_white = '#FEFEFE'
# pl_background = '#162B50'
# pl_text = '#72a3f7'
# pl_line_color = '#293a6b'

# sns.set_theme(
#     style={
#         'axes.edgecolor': pl_line_color,
#         'axes.facecolor': pl_background,
#         'axes.labelcolor': pl_white,
#         'xtick.color': pl_white,
#         'ytick.color': pl_white,
#         'figure.facecolor':pl_background,
#         'grid.color': pl_background,
#         'grid.linestyle': '-',
#         'legend.facecolor':pl_background,
#         'text.color': pl_white
#      }
#     )

# # Gen 1
# color_scheme = ['#FF5959',
#                '#F5AC78',
#                '#FAE078',
#                 '#8EC7BC',
#                '#FA92B2'] if poke_gen=='Gen1' else ['#FF5959',
#                                                     '#F5AC78',
#                                                     '#FAE078',
#                                                     '#9DB7F5',
#                                                     '#A7DB8D',
#                                                     '#FA92B2']

# gen_map = {
#     'Gen1':'https://github.com/Blandalytics/hockeymon/blob/main/data/hockey_pokemon_gen1.csv?raw=true',
#     'Gen2':'https://github.com/Blandalytics/hockeymon/blob/main/data/hockey_pokemon_gen2.csv?raw=true'
# }

# @st.cache_data
# def load_data(gen):
#     return pd.read_csv(gen_map[gen], encoding='latin1')
# sim_frame = load_data(poke_gen)

@st.cache_data
def load_players():
    return list(pd.read_csv('https://github.com/Blandalytics/hockeymon/blob/main/data/hockey_pokemon_gen1.csv?raw=true', encoding='latin1')['Player'].unique())
players = load_players()

# Player
# players = list(sim_frame['Player'].unique())
default_ix = players.index('Jason Robertson')
player = st.selectbox('Select a player:', players, index=default_ix)
# player='Jason Robertson'

# def similarity_card(player=player, poke_gen=poke_gen):
#     sim_score = sim_frame.loc[sim_frame['Player']==player,'Sim_Score'].values[0]
#     pokemon = sim_frame.loc[sim_frame['Player']==player,'Pokémon'].values[0]
#     pokedex_num = sim_frame.loc[sim_frame['Pokémon']==pokemon,'#'].values[0]
    
#     hockey_stats = {'Time On Ice':'TOI_GP',
#                     'EV Offense':'xEVO_GAR', 
#                     'EV Defense':'xEVD_GAR', 
#                     'Spec. Teams':'xST_GAR',
#                     'Penalties':'Pens_GAR'} if poke_gen=='Gen1' else {'Time On Ice':'TOI_GP',
#                                                                       'EV Offense':'xEVO_GAR', 
#                                                                       'EV Defense':'xEVD_GAR', 
#                                                                       'PP Offense':'xPPO_GAR',
#                                                                       'PK Defense':'xSHD_GAR',
#                                                                       'Penalties':'Pens_GAR'}
    
    
#     poke_stats = ['HP','Attack', 'Defense', 
#                   'Special','Speed'] if poke_gen=='Gen1' else ['HP','Attack', 'Defense', 
#                                                                'Sp. Attack','Sp. Defense','Speed']
    
#     fig = plt.figure(figsize=(8,10))
    
#     # Parameters to divide card
#     grid_height = 3
#     grid_width = 6
    
#     # Divide card into tiles
#     grid = plt.GridSpec(grid_height, grid_width, 
#                         hspace=0, wspace=1.5,
#                         height_ratios=[6,6,1])
    
#     title_ax = plt.subplot(grid[0, :3])
#     title_ax.text(0.4,0.9,f"{player}'s",size=25,va='center',ha='center')
#     title_ax.text(0.4,0.8,f"Most Similar {poke_gen} Pokémon:",size=15,va='center',ha='center')
#     title_ax.text(0.4,0.6,f"{pokemon}",size=50,va='center',ha='center')
#     title_ax.text(0.4,0.35,f"Similarity Score:",size=15,va='center',ha='center')
#     title_ax.text(0.4,0.2,f"{sim_score:.0f}/100",size=40,va='center',ha='center')
#     title_ax.axis('off')
    
#     poke_loc = f'https://github.com/Blandalytics/hockeymon/blob/main/poke_pics/{pokedex_num}.png?raw=true'
#     poke_pic = Image.open(urllib.request.urlopen(poke_loc))
#     img_ax = plt.subplot(grid[0, 3:])
#     img_ax.imshow(poke_pic)
#     img_ax.axis('off')
    
#     h_stats_ax = plt.subplot(grid[1, :3])
#     sns.barplot(x=list(sim_frame.loc[sim_frame['Player']==player,
#                                      [x+'_scale' for x in hockey_stats.values()]].values[0]),
#                 y=list(hockey_stats.keys()),
#                 palette=color_scheme,
#                 ax=h_stats_ax
#                )
#     for chart_stat in hockey_stats.keys():
#         chart_val = sim_frame.loc[sim_frame['Player']==player,hockey_stats[chart_stat]+'_scale'].values[0]
#         text_val = sim_frame.loc[sim_frame['Player']==player,hockey_stats[chart_stat]].values[0]
#         h_stats_ax.text(chart_val-0.05 if chart_val>=0.3 else chart_val+0.05,
#                 list(hockey_stats.keys()).index(chart_stat),
#                 f'{text_val:.1f}',
#                 ha='right' if chart_val>=0.3 else 'left',
#                 va='center',
#                 color=color_scheme[list(hockey_stats.keys()).index(chart_stat)],
#                 bbox=dict(facecolor=pl_background, edgecolor=pl_background),
#                 size=16,
#                 fontweight='bold')
    
#     h_stats_ax.set(xlim=(0,1.2))
#     h_stats_ax.get_xaxis().set_visible(False)
#     plt.yticks(fontsize=12)
#     plt.tick_params(left = False)
    
#     p_stats_ax = plt.subplot(grid[1, 3:])
#     sns.barplot(x=list(sim_frame.loc[sim_frame['Player']==player,
#                                     [x+'_scale' for x in poke_stats]].values[0]),
#                 y=poke_stats,
#                 palette=color_scheme,
#                 ax=p_stats_ax
#                )
#     for chart_stat in poke_stats:
#         chart_val = sim_frame.loc[sim_frame['Player']==player,chart_stat+'_scale'].values[0]
#         text_val = sim_frame.loc[sim_frame['Player']==player,chart_stat].values[0]
#         p_stats_ax.text(chart_val-0.05 if chart_val>=0.3 else chart_val+0.05,
#                 poke_stats.index(chart_stat),
#                 f'{text_val:.0f}',
#                 ha='right' if chart_val>=0.3 else 'left',
#                 va='center',
#                 color=color_scheme[poke_stats.index(chart_stat)],
#                 bbox=dict(facecolor=pl_background, edgecolor=pl_background),
#                 size=16,
#                 fontweight='bold')
#     p_stats_ax.set(xlim=(0,1.1))
#     p_stats_ax.get_xaxis().set_visible(False)
#     plt.yticks(fontsize=12)
#     plt.tick_params(left = False)
    
#     disclaimer_ax = plt.subplot(grid[2, 0:])
#     gen_1_filler = '(Spec. Teams = xPPO + xSHD) ' if poke_gen=='Gen1' else ''
#     disclaimer_ax.text(0.4,0.5,f"Based on percentile of Evolving-Hockey's xGAR Metrics\n{gen_1_filler}and percentile of Pokémon's stats",size=12,va='center',ha='center')
#     disclaimer_ax.axis('off')
    
#     sns.despine(bottom=True)
#     time.sleep(1)
#     return fig
#     # st.pyplot(fig)
# if poke_gen=='Gen1':
#     st.pyplot(similarity_card())
# else:
card_loc = f"https://github.com/Blandalytics/hockeymon/blob/main/hockeymon_cards/{player.replace(' ','%20')}-{poke_gen}.png?raw=true"
hockeymon_card = Image.open(urllib.request.urlopen(card_loc))
st.image(hockeymon_card)

st.write("Make sure to subscribe to [Evolving-Hockey](https://evolving-hockey.com/) and follow me [@Blandalytics](https://twitter.com/blandalytics)!\n\nIf you REALLY like this, [Buy me a Coffee!](https://bmc.link/blandalytics)")
