
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback_context
import popular_data_skills.dashboard.helpers_plots as plots


# check out
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# server = app.server
app.config.suppress_callback_exceptions = True


# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# ,external_stylesheets=[dbc.themes.BOOTSTRAP]

# the style arguments for the sidebar. We use position:fixed and a fixed width

job_profile1 = plots.JobFilter('analyst', '5+', 'phd', )
job_profile2 = plots.JobFilter('scientist', '5+', 'phd', )
degree_list = job_profile1.degree_list
experience_list = job_profile1.experience_list
group_list = job_profile1.group_list
# degree_list = ['not_specified','bs','ms','phd']
# experience_list = ['0', '1', '2', '3-5', '5+']
# group_list = ['Topic', 'Skills', 'Business_area', 'Languages', 'Tools', 'Degree', 'Other']


comparision_group = 'Skills'

card_titles = 'h1'

header_height, footer_height = "3rem", "10rem"
sidebar_width = "16rem"
# ACCORDIAN_STYLE= {
#     "background-color": "#80A8D6",
#     #"font-size": "4rem",


# }

SIDEBAR_STYLE = {
    # "position": "fixed",
    # "top": 0,
    # "left": 0,
    # "bottom": 0,
    # "width": sidebar_width,
    # "padding": "2rem 1rem",
    # "position": "fixed",
    "background-color": "#f8f9fa",
}

HEADER_STYLE = {
    # #"position": "fixed",
    # "top": 0,
    # "left": sidebar_width,
    # "right": 0,
    # "height": header_height,
    # "padding": "2rem 1rem",
    # "background-color": "#DBE2EA",
}

# CONTENT_STYLE = {
#     "margin-top": header_height,
#     "margin-left": sidebar_width,
#     "margin-right": "2rem",
#     "margin-bottom": footer_height,
#     "padding": "1rem 1rem",
# }

# FOOTER_STYLE = {
#     "position": "fixed",
#     "bottom": 0,
#     "left": 0,
#     "right": 0,
#     "height": footer_height,
#     "padding": "1rem 1rem",
#     "background-color": "gray",
# }
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    # "margin-left": sidebar_width,
    #    "margin-right": "1rem",
    #     "padding": "1rem 1rem",
    # "background-color": "#D0DEEE"
}
# Components
header = html.Div([
    html.H2("In Demand Data Skills")],
)

navbar = html.Div([dbc.NavbarSimple(
    # children=[
    #     dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    #     dbc.DropdownMenu(
    #         children=[
    #             #dbc.DropdownMenuItem("More pages", header=True),
    #            # dbc.DropdownMenuItem("Page 2", href="#"),
    #             #dbc.DropdownMenuItem("Page 3", href="#"),
    #         ],
    #         nav=False,
    #         in_navbar=False,
    #         label="More",
    #     ),
    # ],
    brand="In Demand Data Skills",
    brand_href="#",
    color="primary",
    dark=True,
    fixed='top',

),
], style={"height": "2.5rem"})


def radio_buttons(component_id):
    return html.Div(
        dbc.RadioItems(
            options=[
                {"label": "Data Scientist", "value": "scientist"},
                {"label": "Data Analyst", "value": "analyst"},
            ],
            value="scientist",
            id=component_id,
            inline=True,
            style={'color': 'primary'}
        ),
    )


# def drop_down_menu(component_id, component_options, component_value):
#     return dcc.Dropdown(
#         id= component_id,
#         options=component_options,
#         value=component_value,
#     )


def profile_select_card(card_id, title, job_id, experience_id, degree_id, button_text, button_id,):
    return html.Div(children=[
        # dbc.Card(
        #     dbc.CardBody([html.Div([
        dbc.Row([
            # html.P(title, className="lead"),
                    dbc.RadioItems(
                        options=[
                            {"label": "Data Scientist", "value": "scientist"},
                            {"label": "Data Analyst",
                             "value": "analyst"},
                        ],
                        value="scientist",
                        id=job_id,
                        inline=True,
                    ),

                    dbc.Col([
                        dbc.Label("Experience"),
                        dcc.Dropdown(
                            id=experience_id,
                            options=[{'label': i, 'value': i}
                                     for i in experience_list],
                            value='5+',
                        ),
                    ], width=6, align='center', className='mt-4',
                    ),

                    dbc.Col([
                        dbc.Label("Degree"),
                        dcc.Dropdown(
                            id=degree_id,
                            options=[{'label': i.capitalize(), 'value': i}
                                     for i in degree_list],
                            value='phd',
                        ),
                    ], width=6, align='center', className='mt-4',
                    ),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button(button_text, n_clicks=0, color="primary",
                                       className="w-100 m-2", id=button_id,),
                        ], width=12, align='center'),
                    ],),
                    ],),
        # ]),

        #     ]),
        # ),
    ], id=card_id, style={"display": "block"},)


profile1_select_card = profile_select_card(title="Job Profile 1",
                                           job_id="job_profile1_job",
                                           experience_id="job_profile1_experience",
                                           degree_id="job_profile1_degree",
                                           button_text="Find Skills",
                                           button_id="job_profile1_button",
                                           card_id="profile1_select_card_id",
                                           )
profile2_select_card = profile_select_card(title="Job Profile 2",
                                           job_id="job_profile2_job",
                                           experience_id="job_profile2_experience",
                                           degree_id="job_profile2_degree",
                                           button_text="Compare",
                                           button_id="job_profile2_button",
                                           card_id="profile2_select_card_id",

                                           )

# layout_button = html.Div(
#     [
#         dbc.RadioItems(
#             id="layout_button_id",
#             className="btn-group",
#             inputClassName="btn-check",
#             labelClassName="btn btn-outline-primary",
#             labelCheckedClassName="active",
#             options=[
#                 {"label": "1 Profile", "value": False},
#                 {"label": "Compare", "value": True},

#             ],
#             value=True,
#         ),
#     ],className="layout_buttons",
# )


layout_button = html.Div(
    [
        dbc.RadioItems(
            id="layout_button_id",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "1 Profile", "value": False},
                {"label": "Compare", "value": True},
            ],
            value=True,
        ),
    ], className="radio-group", style={'width': '100%'},
)


sidebar = (
    html.Div([
        dbc.Row([
            dbc.Col([
                html.P(
                    "Choose '1 Profile' to find most in demand skills. Choose 'Compare' to compare two job profiles", className=""),
                layout_button,
                html.P("Choose Profiles below:", className="m-2"),
                # profile1_select_card,
                # html.Hr(className="pb-25"),
                # html.P("Choose job profile 2 to compare.", className=""),
                # profile2_select_card,
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.P(
                                    "Select job profile for most in demand skills:"),
                                profile1_select_card,
                            ],
                            title="JOB PROFILE 1",
                        ),
                        dbc.AccordionItem(
                            [
                                html.P("Select job profile to compare:"),
                                profile2_select_card,
                            ],
                            title="JOB PROFILE 2", id="accord_item2",
                        ),
                    ], start_collapsed=True, className='accordianitem2',)

                # dbc.Nav(
                #     [
                #         dbc.NavLink("Home", href="/", active="exact"),
                #         dbc.NavLink("Page 1", href="/page-1", active="exact"),
                #         dbc.NavLink("Page 2", href="/page-2", active="exact"),
                #     ],
                #     vertical=True,
                #     pills=True,
                # ),
            ]),
        ]),
    ], className="p-2 h-100",
        style=SIDEBAR_STYLE,
    )
)


# col-xs-4 col-md-3 col-lg-3 col-xxl-3
description_text = (
    html.Div(
        dbc.Card(
            dbc.CardBody(
                html.P("Most in demand skills have been taken from job posts on linked in and ranked. Select a job profile in the sidebar to see the most in demand skills. You can compare different job profiles by filling out job profile 2. "
                       )
            )
        ), className="p-2",
    )
)

# treeplot=job_profile1.tree_map()


def plot_card(title: str, plot_id: str, plot):
    return html.Div(
        dbc.Card(
            dbc.CardBody([
                html.H2(title),
                dcc.Graph(id=plot_id, figure=plot)])
        ), className="p-2",
    )


# treemap = (
#     html.Div(
#         dbc.Card(
#             dbc.CardBody([
#                 html.H2("Profile 1"),
#                 dcc.Graph(figure=job_profile1.tree_map())])
#         ),className="p-2",
#     )
# )
treemap1_card = plot_card(
    title="Profile 1", plot_id="profile1_treemap", plot=job_profile1.tree_map())
treemap2_card = plot_card(
    title="Profile 2", plot_id="profile2_treemap", plot=job_profile2.tree_map())
treemap3_card = plot_card(title="Most in demand Skills",
                          plot_id="profile1_single_treemap", plot=job_profile1.tree_map())

# barplot = ""
# grouped_barplot = (html.Div(
#         dbc.Card(
#             dbc.CardBody([
#                 html.P("Compare skills",),
#                 dcc.Graph(figure=job_profile1.grouped_bar_plot(job_profile2, comparision_group)),
#                 ])
#         ),className="p-2",
#     )
# )
grouped_barplot = plot_card(title="Compare skills", plot_id="grouped_plot",
                            plot=job_profile1.grouped_bar_plot(job_profile2, comparision_group))


# comparision_barplot = (html.Div(
#         dbc.Card(
#             dbc.CardBody([
#                 html.P("Most popular Skills"),
#                 dcc.Graph(figure=job_profile1.most_demand_compare_barplot(job_profile2, comparision_group))])
#         ),className="p-2",
#     )
# )
comparision_barplot = plot_card(title="Most popular Skills", plot_id="comparision_plot",
                                plot=job_profile1.most_demand_compare_barplot(job_profile2, comparision_group))

barplot1 = plot_card(title="Most popular Skills",
                     plot_id="bar_plot_popular", plot=job_profile1.bar_plot('all'))
barplot2 = plot_card(title="Group Skills", plot_id="bar_plot_group",
                     plot=job_profile1.bar_plot(comparision_group))


skills_dropdown = (
    html.Div(
        dbc.Card(
            dbc.CardBody([
                html.Div(
                    html.P("Choose group to compare"), className="lead"),
                html.Div(
                    dcc.Dropdown(
                        id='skill_dropdown',
                        options=[{'label': group.capitalize(), 'value': group}
                                 for group in group_list],
                        value='Skills',
                    )
                )
            ],)
        ), className="px-3",
    )
)

# Main Contents layout:
# Plots, text and skills dropdown
# CCS - structure, padding and margin
main_contents = html.Div([
    dbc.Row([
        dbc.Col([
            description_text,
        ]),
    ],),

    dbc.Row([
        dbc.Col([
            treemap1_card], width=6,),
        dbc.Col([
            treemap2_card], width=6,),
    ],
        className="g-0 m-0 p-0"),

    dbc.Row([
        skills_dropdown],
    ),

    dbc.Row([
        dbc.Col([
            comparision_barplot, ], width=6,),
        dbc.Col([
            grouped_barplot, ], width=6,), ],
            className="g-0 "),


], id="compare_page", className="h-75", style=CONTENT_STYLE),


main_contents_single = html.Div([
    dbc.Row([
        dbc.Col([
            description_text,
        ]),
    ],),

    dbc.Row([
        dbc.Col([
            treemap3_card], width=12,),

    ],
        className="g-0 m-0 p-0"),

    dbc.Row([
        skills_dropdown],
    ),

    dbc.Row([
        dbc.Col([
            barplot1, ], width=6,),
        dbc.Col([
            barplot2, ], width=6,), ],
            className="g-0 "),


], id="compare_page", className="h-75", style=CONTENT_STYLE),


# General top level layout:
# Navbar, side bar, main contents.
# CCS - structure, padding and margin
app.layout = html.Div([
    # html.Link(
    #     rel='stylesheet',
    #     href='assests\custom.css'),
    dbc.Row([dbc.Col(
            navbar)
    ]),

    dbc.Row([
        dbc.Col(children=[
            html.Div(
                sidebar), ], width=3, className="position-fixed mt-3", id="sidebar_layout"),
        dbc.Col(children=[
            html.Div(
                main_contents)], width={"size": 9, "order": "last", "offset": 3}, className="mt-3", id="plot_layout"),
    ], className="g-0",
    ),

    # dbc.Col(children= [
    #     html.Div(
    #         sidebar)],width=3, className="position-fixed mt-3", id="sidebar_layout"),


    #  sidebar]), xs=5, md=3,lg=3, xxl=3



    # dbc.Row(
    #     [
    #         dbc.Col(html.Div("One of four columns"), width=6, lg=3),
    #         dbc.Col(html.Div("One of four columns"), width=6, lg=3),
    #         dbc.Col(html.Div("One of four columns"), width=6, lg=3),
    #         dbc.Col(html.Div("One of four columns"), width=6, lg=3),
    #     ]
    # ),
]
)

# @app.callback(Output('button', 'disabled'),
#              [Input('dropdown', 'value')])
# def set_button_enabled_state(on_off):
#     return on_off


# @app.server.route('/assests/<path:path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'assests')
#     return send_from_directory(static_folder, path)

# change layout
@app.callback(
    Output("plot_layout", "children"),
    #Output("job_profile2_button", "disabled"),
    Output("accord_item2", "style"),
    Input("layout_button_id", 'value'),
)
def change_layout(layout_button_id):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if "layout_button_id" in changed_id:
        if layout_button_id:
            button_state = False
            card_visability = {"display": "inline"}
            return main_contents, card_visability
        else:
            button_state = True
            card_visability = {"display": "none"}
            return main_contents_single, card_visability


# compare callback
@app.callback(
    [
        Output("profile1_treemap", "figure"),
        Output("profile2_treemap", "figure"),
        Output("grouped_plot", "figure"),
        Output("comparision_plot", "figure"),


    ],
    [
        Input("job_profile1_button", 'n_clicks'),
        Input("skill_dropdown", 'value'),
        Input("job_profile2_button", 'n_clicks'),

    ],
    [
        State("job_profile1_job", 'value'),
        State("job_profile1_experience", 'value'),
        State("job_profile1_degree", 'value'),
        State("job_profile2_job", 'value'),
        State("job_profile2_experience", 'value'),
        State("job_profile2_degree", 'value'),
    ],
)
def on_click(job_profile1_button, skill_dropdown, job_profile2_button, job_profile1_job, job_profile1_experience, job_profile1_degree, job_profile2_job, job_profile2_experience, job_profile2_degree):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if ("job_profile1_button" in changed_id) or ("skill_dropdown" in changed_id) or ("job_profile2_button" in changed_id):
        job_profile1 = plots.JobFilter(
            job_profile1_job, job_profile1_experience, job_profile1_degree)
        job_profile2 = plots.JobFilter(
            job_profile2_job, job_profile2_experience, job_profile2_degree)

        treemap1 = job_profile1.tree_map()
        treemap2 = job_profile2.tree_map()
        grouped_plot = job_profile1.grouped_bar_plot(
            job_profile2, skill_dropdown)
        comparision_plot = job_profile1.most_demand_compare_barplot(
            job_profile2, skill_dropdown)

    return treemap1,  treemap2, grouped_plot,  comparision_plot,


# Single callback
@app.callback(
    [
        Output("profile1_single_treemap", "figure"),
        Output("bar_plot_popular", "figure"),
        Output("bar_plot_group", "figure"),

    ],
    [
        Input("job_profile1_button", 'n_clicks'),
        Input("skill_dropdown", 'value'),
    ],
    [
        State("job_profile1_job", 'value'),
        State("job_profile1_experience", 'value'),
        State("job_profile1_degree", 'value'),
    ],
)
def on_click(job_profile1_button, skill_dropdown, job_profile1_job, job_profile1_experience, job_profile1_degree):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if ("job_profile1_button" in changed_id) or ("skill_dropdown" in changed_id):
        job_profile1 = plots.JobFilter(
            job_profile1_job, job_profile1_experience, job_profile1_degree)

        treemap3 = job_profile1.tree_map()
        bar_plot_popular = job_profile1.bar_plot('all')
        bar_plot_group = job_profile1.bar_plot(skill_dropdown)

    return treemap3, bar_plot_popular, bar_plot_group

    # Output("profile1_single_treemap", "figure"),
    # Output("bar_plot_popular", "figure"),
    # Output("bar_plot_group", "figure"),

    # treemap3 = job_profile1.tree_map()
    # bar_plot_in_demand = job_profile1.bar_plot('all')
    # bar_plot_by_group = job_profile1.bar_plot(skill_dropdown)


# @app.callback(Output("compare_page", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == "/":
#         return compare_page
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )



app.run_server(port=8888)
