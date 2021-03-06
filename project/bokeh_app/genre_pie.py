import pandas as pd
import numpy as np

import pickle

import os

from bokeh.io import output_file, show, export_svgs
from bokeh.layouts import widgetbox, row, column,layout
from bokeh.models.widgets import Select, CheckboxGroup,RangeSlider, Slider
from bokeh.models import ColumnDataSource, HoverTool, Div, Range1d
from bokeh.plotting import curdoc, figure
from bokeh.client import push_session
from bokeh.charts import Donut

from bokeh.resources import CDN
from bokeh.embed import file_html




f = open('../cache/dataframe-final', 'rb')
df = pickle.load(f)



genre_color = {'blues': '#75bbfd', 'country': '#653700', 'electronica': '#9a0eea', 'folk': '#f97306', 'jazz': '#fac205',
               'pop': '#ff81c0', 'metal': '#000000', 'rock': '#2242c7', 'orchestral': '#929591', 'hiphop': '#e50000',
               'reggae': '#02ab2e', 'world': '#a0bf16'}


def song_selected():
    (start, end) = year_slider.value

    if 1 in checkbox_year.active:
        selected=df[(df.year>=start) & (df.year<=end) | (df.year==0)]
    else:
        selected = df[(df.year >= start) & (df.year <= end)]

    if 0 not in checkbox_year.active:
        selected =selected[df.artist_latitude>=0]


    return selected



def update(attr, old, new):
    layout.children[1] = create_figure()



checkbox_year = CheckboxGroup(labels=["Show songs with missing location","Show songs with missing year"], active=[0])
checkbox_year.on_change('active', update)

year_slider = RangeSlider(start=1940, end=2010, value=(1940,2010), step=5, title="year")
year_slider.on_change('value', update)



def create_figure():


    data = song_selected()

    p = figure(plot_height=400, plot_width=400)
    if len(data) > 0:



        #title = 'The {} most {} songs'.format( var_slider.value,type.value)


        count = data.genre.value_counts()

        colors = [genre_color[x] for x in count.index.sort_values()]

        p = Donut(count, label='index', color=colors, height=400, width=400,hover_text='#songs')

        p.title.text = "#songs = {}".format(len(data))


    return p


controls = widgetbox([checkbox_year,year_slider], width=200)


layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Music-Genre"

