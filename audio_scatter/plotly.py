import plotly.graph_objs as go
import plotly.express as px
from IPython.display import HTML, Audio, update_display, display
from . import play, create_player


def audio_scatter(data, x='x', y='y', audio_path='audio_path', label=None, player_id=None, normalize=True, circle_radius=0.03, figsize=None, start=None, stop=None, **kwargs):
    if player_id is None:
        player_id = 1234567
        create_player(player_id)

    p = px.scatter(data, x=x, y=y,text=label, **kwargs)
    fig = go.FigureWidget(p)

    def hover_fn(trace, points, *_):
        if points.point_inds:
            ind = points.point_inds[0]
            r = data.iloc[ind]
            if start is not None and stop is not None:
                _start = r[start]
                _stop = r[stop]
            else:
                _start = None
                _stop = None
            play(r[audio_path], player_id, normalize=normalize, start=_start, stop=_stop)

    for f in fig.data:
        f.on_hover(hover_fn)

    return fig 
   