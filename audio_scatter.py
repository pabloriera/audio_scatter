import matplotlib.pyplot as plt
from IPython.display import HTML, Audio, update_display
import seaborn as sns
import numpy as np

def create_player(player_id):
    html = """<audio controls="true"></audio>"""
    display_handle = display(HTML(html),display_id=player_id)
    
def play(filename, player_id, autoplay=True):
    update_display(Audio(filename,autoplay=autoplay),display_id=player_id)    
    
def audio_scatter(data, x='x', y='y', c='c', wav='wav', alpha=1, player_id=None, figsize=None,legend=False):
    assert player_id is not None
    
    fig, ax = plt.subplots(1, figsize=figsize)
    sns.scatterplot(x=x, y=y, hue=c, data=data, ax=ax, alpha=alpha, legend=legend)
    tx = ax.text(0, 0, "", va="bottom", ha="left")
    circ = plt.Circle((0, 0), max(np.abs(data[x]).max(), np.abs(data[y]).max()) / 100, facecolor='none', edgecolor='k')
    ax.add_artist(circ)
    def onclick(event):
        d = np.square(event.xdata - data[x].values) + np.square(event.ydata - data[y].values)
        ix = np.argmin(d)
        r = data.iloc[ix]
        tx.set_text('{} ({})'.format(r.name, r.c))
        tx.set_x(event.xdata)
        tx.set_y(event.ydata)
        circ.center = (r.x, r.y)
        fig.canvas.draw()
        play(r.wav,player_id)

    fig.canvas.mpl_connect('button_press_event', onclick)