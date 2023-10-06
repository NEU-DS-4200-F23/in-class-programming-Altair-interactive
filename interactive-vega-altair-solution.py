# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
#  # Interactive Vega-Altair with Jupyter Widgets
#  This notebook will guide you through using [Vega-Altair](https://altair-viz.github.io/) along with [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/)

# %% [markdown]
# # Setup
# First, import what we need.

# %%
import math
import altair as alt
from altair import datum
import pandas as pd
import numpy as np
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from vega_datasets import data

# %% [markdown]
# Then, check versions of installed packages.

# %%
'ipywidgets ' + widgets.__version__ + 
', altair ' + alt.__version__ + 
', pandas ' + pd.__version__ + 
', numpy ' + np.__version__

# %% [markdown]
# Allow Altair to use more than 5000 rows

# %%
alt.data_transformers.enable('vegafusion')

# %%
alt.renderers.enable('png')


# %% [markdown]
# # Jupyter Widgets Examples

# %% [markdown]
# We are going to use [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/) to create basic interactions with Altair. You can see the documentation for [all the available widgets here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html). Note that you should use the decorator syntax, as the other approach [is more complicated with Altair](https://github.com/altair-viz/altair/issues/2107). For example, this uses the `@interact` decorator syntax to have a `Text` widget run a function we define:

# %%
@interact(
    str1=widgets.Text(
        value='Hello',
        description='Input string 1:'
    )
)
def print10X(str1):
    for i in range (10):
        print(' '.join([str1, str(i)]))



# %% [markdown]
# This is the alternative that doesn't use decorators. Note how it takes more code to do the same thing, and that displaying the output of a Vega-Altair visualization is more problematic than text.

# %%
textWidget = widgets.Text(
    value='Hello World!',
    description='Input string:'
)
output = widgets.Output()

display(textWidget, output)

def print10X(change):
    inputStr = change['new']
    with output:
        print(change)
        for i in range (10):
            print(' '.join([inputStr, str(i)]))

textWidget.observe(print10X, names='value')


# %%
@interact(
    str1=widgets.Text(
        value='Hello',
        description='Input string 1:'
    ),
    str2=widgets.Text(
        value='World!',
        description='Input string 2:'
    ),
)
def print10XPair(str1, str2):
    for i in range (10):
        print(' '.join([str1, str2, str(i)]))


# %% [markdown]
# Here's another example using an `IntSlider`:

# %%
@interact(
    x=widgets.IntSlider(
        value=7,
        min=0,
        max=10,
        step=1,
        description='x:'
    )
)
def times10(x):
    print(x * 10)


# %% [markdown]
# # Jupyter Widgets and Altair

# %% [markdown]
# ## Birdstrikes data barcharts
#
# We are going to load the birdstrikes dataset from `vega-datasets`.

# %%
birdStrikesDF = data.birdstrikes()
birdStrikesDF

# %% [markdown]
# Now, let's create a bar chart of some of the data.

# %%
alt.Chart(birdStrikesDF).mark_bar().encode(
    x='When__Phase_of_flight',
    y='count()'
)

# %% [markdown]
# Let's add a title to describe this chart.

# %%
alt.Chart(
        birdStrikesDF,
        title=alt.Title(
            'Bird Strikes Dataset'
        )
    ).mark_bar().encode(
    x='When__Phase_of_flight',
    y='count()'
)


# %% [markdown]
# That's only one of the attributes. Can we use Jupyter Widgets to select arbitrary ones?

# %%
@interact(xcol=widgets.Dropdown(
    options=list(birdStrikesDF.columns),
    value='When__Phase_of_flight',
    description='Column:',
))
def barChart(xcol):
    return alt.Chart(
            birdStrikesDF,
            title=alt.Title(
                'Bird Strikes Dataset'
            )
        ).mark_bar().encode(
        x=xcol,
        y='count()'
    )


# %% [markdown]
# Can we look at just bird strikes that were within certain cost ranges?
#
# First, let's set up the column and range of values we're working with.

# %%
costCol = 'Cost__Total_$'
costRangeInData=[# thousands
    math.floor(birdStrikesDF[costCol].min() / 1000), 
    math.ceil(birdStrikesDF[costCol].max() / 1000)
]
costRangeInData


# %%
@interact(
    xcol=widgets.Dropdown(
        options=list(birdStrikesDF.columns),
        value='When__Phase_of_flight',
        description='Column:',
    ),
    costRange=widgets.IntRangeSlider(
        value=costRangeInData,
        min=costRangeInData[0],
        max=costRangeInData[1],
        step=1,
        description='Cost range:'
    )
)
def barChartRanges(xcol, costRange):
    return alt.Chart(
        birdStrikesDF,
        title=alt.Title(
            'Bird Strikes Dataset',
            subtitle='With costs $' + 
            str(costRange[0]) + '–' + 
            str(costRange[1]) + 'k'
        )
    ).transform_filter(
        ((datum[costCol] >= (costRange[0] * 1000)) &
         (datum[costCol] <= (costRange[1] * 1000)))
    ).mark_bar().encode(
        x=xcol,
        y='count()'
    )


# %% [markdown]
# ## Iris data scatterplots
#
# We are going to load the iris dataset from `vega-datasets`.

# %%
irisDF = data.iris()
irisDF


# %% [markdown]
# Creating a simple scatterplot

# %%
def irisScatter():
    irisChart = alt.Chart(irisDF)
    
    points = irisChart.mark_point().encode(
        x='sepalLength',
        y='petalLength',
    )

    return points
irisScatter()


# %% [markdown]
# Adding a tooltip and color. You can use any color from the [valid Vega-Lite color schemes](https://vega.github.io/vega/docs/schemes/
# ).

# %%
def irisScatter():
    irisChart = alt.Chart(irisDF)
    
    points = irisChart.mark_point().encode(
        x='sepalLength',
        y='petalLength',
        color=alt.Color('sepalWidth', scale=alt.Scale(scheme='purples')),
        tooltip=['sepalLength', 'petalLength', 'sepalWidth', 'petalWidth']
    )

    return points
irisScatter()


# %% [markdown]
# Now, let's add some a [brush](https://altair-viz.github.io/gallery/interactive_brush.html) for some interactivity. This is one of many types of [interactivity Vega-Altair can provide](https://altair-viz.github.io/user_guide/interactions.html).

# %%
def irisBrushScatter():
    brush = alt.selection_interval(encodings=['x', 'y'])
    
    irisChart = alt.Chart(irisDF)
    
    points = irisChart.mark_point().encode(
        x='sepalLength',
        y='petalLength',
        color=alt.Color('sepalWidth', scale=alt.Scale(scheme='purples')),
        size=alt.condition(brush, alt.value(50), alt.value(1)),
        tooltip=['sepalLength', 'petalLength', 'sepalWidth', 'petalWidth']
    ).add_params(
        brush
    )
    
    return points
irisBrushScatter()

# %% [markdown]
# Finally, lets add a line to show the median value.

# %%
brush = alt.selection_interval(encodings=['x', 'y'])

irisChart = alt.Chart()

points = irisChart.mark_point().encode(
    x='sepalLength',
    y='petalLength',
    color=alt.Color('sepalWidth', scale=alt.Scale(scheme='purples')),
    size=alt.condition(brush, alt.value(50), alt.value(1)),
    tooltip=['sepalLength', 'petalLength', 'sepalWidth', 'petalWidth']
).add_params(
    brush
)

meanLine = alt.Chart().mark_rule(color='black', opacity=.5).encode(
    x=alt.X('median(sepalLength):Q', scale=alt.Scale(zero=False)),
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

alt.layer(points, meanLine, data=irisDF)

# %% [markdown]
# There you go! All done.
