import streamlit as st
import pandas as pd
import numpy as np
import requests
import random
import seaborn as sns
import matplotlib.pyplot as plt


title = st.title('Pokemon Explorer')

pokemon_number = st.text_input('Chose a pokemon number')

if 'rand_num' not in st.session_state.keys():
    st.session_state['rand_num'] = random.randint(1,1025)
    
rand = st.session_state['rand_num']
    

def pokemon(pokemon_number):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/'
    response = requests.get(url)
    pokemon = response.json()

    return pokemon
    

try:
    pokemon1 = pokemon(pokemon_number)
    pokemon2 = pokemon(str(rand))

    

    image1 = pokemon1['sprites']['other']['official-artwork']['front_default']
    image2 = pokemon2['sprites']['other']['official-artwork']['front_default']



    poke = pd.DataFrame(columns=['HP', 'Attack', 'Defense', 'Speacial Attack', 'Special Defense', 'Speed'])
    poke.loc[0] = [ pokemon1['stats'][0]['base_stat'], pokemon1['stats'][1]['base_stat'], pokemon1['stats'][2]['base_stat'], pokemon1['stats'][3]['base_stat'], pokemon1['stats'][4]['base_stat'], pokemon1['stats'][5]['base_stat']]
    poke.loc[1] = [ pokemon2['stats'][0]['base_stat'], pokemon2['stats'][1]['base_stat'], pokemon2['stats'][2]['base_stat'], pokemon2['stats'][3]['base_stat'], pokemon2['stats'][4]['base_stat'], pokemon2['stats'][5]['base_stat']]
    

    
    header = st.header(f"{pokemon1['name'].upper()} VS {pokemon2['name'].upper()}")


    # Pictures & Audio
    cola, colb = st.columns(2)
    with cola:
        st.image(image1)
        st.audio(pokemon1['cries']['latest'], format="audio/wav", start_time=0, sample_rate=None)
    with colb:
        st.image(image2)
        st.audio(pokemon2['cries']['latest'], format="audio/wav", start_time=0, sample_rate=None)




    # Height Comparison Graph
    height = {'Pokemon':[pokemon1['name'],pokemon2['name']], 'Height':[pokemon1['height'],pokemon2['height']]}
    height_data = pd.DataFrame( data=height)
    
    fig, ax = plt.subplots(1, figsize=(10,10))

    h_graph = sns.barplot(data=height_data,
                          x = 'Pokemon',
                          y='Height',
                          ax=ax)
    
    ax.set_title('Height')



    labels = np.array(['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed'])

    # Extract stats for both Pokémon
    stats1 = poke.loc[0]
    stats2 = poke.loc[1]
    

    # Calculate angles for the radar chart
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

    # Complete the loop
    stats1 = np.concatenate((stats1, [stats1[0]]))
    stats2 = np.concatenate((stats2, [stats2[0]]))
    angles += angles[:1]


    fig1 = plt.figure()
    ax = fig1.add_subplot(111, polar=True)

    # Plot data for the first Pokémon
    ax.plot(angles, stats1, 'o-', linewidth=2, label=pokemon1['name'])
    ax.fill(angles, stats1, alpha=0.25)

    # Plot data for the second Pokémon
    ax.plot(angles, stats2, 'o-', linewidth=2, label=pokemon2['name'])
    ax.fill(angles, stats2, alpha=0.25)

    # Set the labels for each axis
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    # Add a legend to differentiate between the two Pokémon
    ax.legend(loc='upper right')

    ax.grid(True)


    st.pyplot(fig1)
 
    st.pyplot(fig)


    
    

except:
    pass
