import matplotlib.pyplot as plt
from matplotlib import patches
from IPython.display import HTML, Audio, update_display, display
import seaborn as sns
import numpy as np
from pydub import AudioSegment
import wave
from io import BytesIO


def raw_wav_segment(filename, start, stop):
    audio_segment = AudioSegment.from_file(filename)
    raw_data = audio_segment[start * 1000:stop * 1000].raw_data
    fp = BytesIO()
    wave_data = wave.open(fp, 'wb')
    wave_data.setnchannels(audio_segment.channels)
    wave_data.setsampwidth(audio_segment.sample_width)
    wave_data.setframerate(audio_segment.frame_rate)
    wave_data.setnframes(int(audio_segment.frame_count()))
    wave_data.writeframesraw(raw_data)
    raw_wav = fp.getvalue()
    wave_data.close()
    return raw_wav, audio_segment.frame_rate


def create_player(player_id):
    html = """<audio controls="true"></audio>"""
    display_handle = display(HTML(html), display_id=player_id)


def play(filename, player_id, autoplay=True, normalize=True, start=None, stop=None):
    if start is not None and stop is not None:
        raw_wav, rate = raw_wav_segment(filename, start, stop)
        update_display(Audio(data=raw_wav, autoplay=autoplay,
                       normalize=normalize, rate=rate), display_id=player_id)
    else:
        update_display(Audio(filename, autoplay=autoplay,
                       normalize=normalize), display_id=player_id)


def audio_scatter(data, x='x', y='y', audio_path='audio_path', label=None, player_id=None, normalize=True, circle_radius=0.03, figsize=None, start=None, stop=None, **kwargs):
    assert player_id is not None

    fig, ax = plt.subplots(1, figsize=figsize)
    sns.scatterplot(x=x, y=y, data=data, ax=ax, **kwargs)
    tx = ax.text(0, 0, "", va="bottom", ha="left")
    pr = fig.get_figwidth() / fig.get_figheight()
    new_xy = transform_coords((0, 0), ax, fig)
    circ = patches.Ellipse(new_xy, circle_radius, circle_radius *
                           pr, transform=fig.transFigure, facecolor='none', edgecolor='k')
    ax.add_artist(circ)

    def onclick(event):
<<<<<<< HEAD:audio_scatter/__init__.py
        
        d = np.square(event.xdata - data[x].values) + np.square(event.ydata - data[y].values)
=======
        d = np.square(event.xdata - data[x].values) + \
            np.square(event.ydata - data[y].values)
>>>>>>> 9e3a3bba6ab3ef54a0537a2854196579f3c41473:audio_scatter.py
        ix = np.argmin(d)
        r = data.iloc[ix]
        print(r)
        if label is not None and label in r:
            tx.set_text('{} ({})'.format(r.name, r[label]))      
        else:
            tx.set_text(r.name)
        tx.set_x(event.xdata)
        tx.set_y(event.ydata)
        circ.set_center(transform_coords((r[x], r[y]), ax, fig))
        fig.canvas.draw()
        if start is not None and stop is not None:
            _start = r[start]
            _stop = r[stop]
        else:
            _start = None
            _stop = None
        play(r[audio_path], player_id,
             normalize=normalize, start=_start, stop=_stop)

    fig.canvas.mpl_connect('button_press_event', onclick)


def transform_coords(xy, ax, fig):
    tscale = ax.transScale + (ax.transLimits + ax.transAxes)
    ctscale = tscale.transform_point(xy)
    cfig = fig.transFigure.inverted().transform(ctscale)
    return cfig
