import plotly.graph_objs as go
import plotly.express as px
from IPython.display import HTML, Audio, update_display, display
from . import play, create_player


def audio_scatter(data, x='x', y='y', z=None, audio_path='audio_path', label=None, player_id=None, normalize=True, start=None, stop=None, action='hover', **kwargs):
    if player_id is None:
        player_id = 1234567
        create_player(player_id)

    if z is not None:
        p = px.scatter_3d(data, x=x, y=y, z=z, text=label, **kwargs)
    else:
        p = px.scatter(data, x=x, y=y, text=label, **kwargs)
    fig = go.FigureWidget(p)

    def action_fn(trace, points, *_):
        if points.point_inds:
            ind = points.point_inds[0]
            r = data.iloc[ind]
            if start is not None and stop is not None:
                _start = r[start]
                _stop = r[stop]
            else:
                _start = None
                _stop = None
            play(r[audio_path], player_id,
                 normalize=normalize, start=_start, stop=_stop)

    for f in fig.data:
        if action == 'hover':
            f.on_hover(action_fn)
        elif action == 'click':
            f.on_click(action_fn)

    return fig
