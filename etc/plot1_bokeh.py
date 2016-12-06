from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components

def bokehplot1():
    plot = figure()
    plot.circle([1,2], [3,4])

    # html = file_html(plot, CDN, "my plot")

    script, div = components(plot, CDN)

    return script, div