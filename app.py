import datetime
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
# import dash_reusable_components as drc
import dash_html_components as html
import base64
from PIL import Image
import plotly.express as px
import numpy as np
from io import BytesIO
from dash.exceptions import PreventUpdate
from SVD_Compress import svd_compress
import gzip
import matplotlib.pyplot as plt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])



config = {
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ],
    'displayModeBar': True,
    'modeBarButtons': True,
    'toImageButtonOptions': dict(
        format='png',
        filename='unknown',
        height=500,
        width=700,
        scale=2,
    ),
}



app.layout = html.Div([
    html.H1('Image Convert&Compress Toolkit',
            style={"text-align": "center",
                   "font-family": "fantasy"}),
    html.P(
        'Here, you can upload your images and do convert&compress. For output file,'
        ' you can choose jpeg, png, webp, svg. For compress, you can choose the degree you want.',
        style={"text-align": "center",
               'margin-bottom': "25px",
               "font-family": "monospace"}),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'font-family': "serif",
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dbc.Row(id='output-image-upload',
            no_gutters=True, ),
    dbc.Row([
        dbc.Col(dbc.Card(
            [
                html.H6('Choose Export Type',
                        style={"text-align": "center",
                               "font-size": "18px",
                               "font-weight": "bold",
                               "font-family": "monospace"}),
                dcc.RadioItems(
                    id='format_option',
                    options=[
                        {'label': 'png', 'value': 'png'},
                        {'label': 'svg', 'value': 'svg'},
                        {'label': 'jpeg', 'value': 'jpeg'},
                        {'label': 'webp', 'value': 'webp'},
                    ],
                    labelStyle={'display': 'inline-block'},
                    style={"text-align": "center",
                           "font-family": "monospace",
                           "font-size": "14px"},
                ),
            ],
        )
        ),
        dbc.Col(dbc.Card(
            [
                html.H6('Choose Compress Degree',
                        style={"text-align": "center",
                               "font-size": "18px",
                               "font-weight": "bold",
                               "font-family": "monospace"}),
                dcc.RadioItems(
                    id='compress_option',
                    options=[
                        {'label': 'slightly', 'value': 'little'},
                        {'label': 'moderately', 'value': 'medium'},
                        {'label': 'strongly', 'value': 'high'}
                    ],
                    labelStyle={'display': 'inline-block'},
                    style={"text-align": "center",
                           "font-family": "monospace",
                           "font-size": "14px",
                           'width': '100%'},
                ),
            ],)
        ),
    ]
    ),
]
)


def get_figure(content):
    content = content[content.find(',') + 1:]
    content = base64.b64decode(content)
    imgdata = np.array(Image.open(BytesIO(content)))
    return imgdata


def show_contents(content, filename, date, format, compress):
    if format is None:
        format = filename[filename.find('.')+1:]

    filename = filename[:filename.find('.')]
    if compress is not None:
        fig = svd_compress(content, compress)
    else:
        fig = get_figure(content)
    # fig.update_layout(dragmode="drawrect")

    img = Image.fromarray(fig).tobytes()
    img = "data:image/{};base64,".format(format) + base64.b64encode(img).decode()


    return dbc.Col(
        [
            html.H5(filename,
                    style={"font-family": "monospace",
                           "font-size": "16px"}),
            html.H6(datetime.datetime.fromtimestamp(date),
                    style={"font-family": "monospace"}),
            dcc.Graph(
                figure=px.imshow(fig,
                                 binary_string=True,
                                 template='plotly_dark',
                                 # width=imgdata.shape[1],
                                 # height=imgdata.shape[0]
                                 aspect='auto'
                                 ),
                # figure.layout={'xaxis': False,
                #             'yaxis': False},
                config=config,
            ),
            html.A(
                dbc.Button("Download", id="get", n_clicks=0, outline=True, block=True,
                           style={
                               "font-weight": "bold",
                               "font-family": "monospace",
                               "font-size": "14px"
                           }),
                download=filename+"."+format,
                href=img,
                style={
                    "text-align": "center",
                }
            )
        ]
    )

def gzip_zip_base64(content):

    bytes_com = gzip.compress(str(content).encode("utf-8"))
    base64_data = base64.b64encode(bytes_com)
    back = str(base64_data.decode())
    return back



@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents'),
               Input('format_option', 'value'),
               Input('compress_option', 'value')
               ],
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'),
              )
def update_output(list_of_contents, format, compress, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [show_contents(c, n, d, format, compress)
                    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]

        # b64 = list_of_contents[0]
        # content = base64.b64decode(b64[b64.find(',')+1:])
        # fig = px.imshow(np.array(Image.open(BytesIO(content))))
        # fig.update_layout(dragmode="drawrect")

        # return fig
        return children
    else:
        raise PreventUpdate



if __name__ == '__main__':
    app.run_server(debug=True)
