import matplotlib.pyplot as plt
from matplotlib import patches
from IPython.display import HTML, Audio, update_display
import seaborn as sns
import numpy as np


def create_player(player_id):
    html = """<audio controls="true"></audio>"""
    display_handle = display(HTML(html),display_id=player_id)
    
def play(filename, player_id, autoplay=True):
    update_display(Audio(filename,autoplay=autoplay),display_id=player_id)    
    
def audio_scatter(data, x='x', y='y', audio_path='audio_path', text='text', player_id=None, figsize=None, **kwargs):
    assert player_id is not None
    
    fig, ax = plt.subplots(1, figsize=figsize)
    sns.scatterplot(x=x, y=y, data=data, ax=ax, **kwargs)
    tx = ax.text(0, 0, "", va="bottom", ha="left")
    
    pr = fig.get_figwidth()/fig.get_figheight()
    radius = max(np.abs(data[x]).max(), np.abs(data[y]).max()) / 100
    new_xy = transform_coords((0,0),ax,fig)
    circ = patches.Ellipse(new_xy, radius, radius*pr, transform=fig.transFigure, facecolor='none', edgecolor='k')
    ax.add_artist(circ)
    def onclick(event):
        d = np.square(event.xdata - data[x].values) + np.square(event.ydata - data[y].values)
        ix = np.argmin(d)
        r = data.iloc[ix]
        tx.set_text('{} ({})'.format(r.name, r[text]))
        tx.set_x(event.xdata)
        tx.set_y(event.ydata)
        circ.set_center(transform_coords((r.x, r.y),ax,fig))       
        fig.canvas.draw()
        play(r.audio_path,player_id)

    fig.canvas.mpl_connect('button_press_event', onclick)

def transform_coords(xy,ax,fig):
    tscale = ax.transScale + (ax.transLimits + ax.transAxes)
    ctscale = tscale.transform_point(xy)
    cfig = fig.transFigure.inverted().transform(ctscale)
    return cfig