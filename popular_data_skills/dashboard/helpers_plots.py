import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import popular_data_skills.dashboard.helpers_filter as filter
import popular_data_skills.config.config as config

class JobFilter():

    def __init__(self, job: str, experience: str, degree: str, ):
        # Read the job data into pandas dataframe
        job_data = pd.read_csv(config.FINAL_DATA_FILE, index_col=False)
        self.background_color = "white"

        self.primary_color = "#2fa4e7"
        self.secondary_color = "#b2cddb"
        self.tertiary_color = "#f8f9fa"
        self.highlight_color = "#1e6b97"
        self._job = job
        self._experience = experience
        self._degree = degree
        self._job_list = job_data['job'].unique()
        self._degree_list = sorted(job_data['degree_level'].unique())
        self._experience_list = sorted(job_data['experience'].unique())
        self._group_list = filter.group_list()

        # Add new column no degree
        job_data['no_degree'] = job_data['degree_level'].apply(
            lambda x: 1 if x == 'not_specified' else 0)

        # Drop unuseful columns
        info_columns = ['company_name', 'country', 'job_title', 'location',
                        'date_posted', 'applicant_count', 'job_description_lines', ]
        job_data = job_data.drop(info_columns, axis=1)

        # Filter data as per profile
        filtered_df = filter.filter_df(job_data, job, experience, degree)

        # Drop catagorical columns use to filter df that are no longer needed
        drop_columns = ['job', 'experience', 'degree_level']
        filtered_df = filtered_df.drop(columns=drop_columns)

        # Wrangle df in summary df
        filtered_df = (filtered_df
                       .sum()
                       .sort_values(ascending=False).astype(int)
                       )

        filtered_df = (filtered_df
                       .to_frame()
                       .reset_index()
                       )

        filtered_df['groups'] = filtered_df['index'].apply(
            filter.add_groups).sort_values()
        filtered_df['index'] = filtered_df['index'].replace({'no_degree': 'no degree stated',
                                                            'degree': 'any degree'})

        group_total_df, filtered_df = filter.get_group_totals(filtered_df)

        def get_ratio(row, group_total_df):
            ''' Uses dfs from get_group_totals to calulate percentage of each skill relative to its parent group '''
            mask = group_total_df[group_total_df['groups'] == row['groups']]
            group_total = mask['group_total'].values[0].astype(int)
            # #return the percantage of group
            return ((row['count'] / group_total) * 100).astype(int)

        filtered_df['ratio'] = filtered_df.apply(
            lambda x: get_ratio(x, group_total_df), axis=1)

        filtered_df = filtered_df[filtered_df['ratio'] != 0]

        self.df = filtered_df

    @property
    def job(self):
        return self._job

    @property
    def experience(self):
        return self._experience

    @property
    def degree(self):
        return self._degree

    @property
    def job_list(self):
        return self._job_list

    @property
    def experience_list(self):
        return self._experience_list

    @property
    def degree_list(self):
        return self._degree_list

    @property
    def group_list(self):
        return self._group_list

    def tree_map(self):
        my_color_scale = [(0.00, "white"),
                          (0.50, self.secondary_color),
                          (0.75, self.primary_color),
                          (1.00, self.highlight_color)]

        # ["white",self.primary_color]
        ''' Return tree map of data filtered by parameters giving. '''
        # Create treemap based on filtered dfs
        self.tree_fig = px.treemap(self.df, path=[px.Constant(
            "all"), 'groups', 'index'], values='ratio', labels="images",
            color='ratio',
            color_continuous_scale=my_color_scale,
            color_continuous_midpoint=np.average(self.df["ratio"]),
        )

        self.tree_fig.update_traces(root_color=self.tertiary_color,)
        self.tree_fig.update_layout(margin=dict(t=10, l=5, r=5, b=10)),

        self.tree_fig.data[0]['textfont']['size'] = 25
        self.tree_fig.update_coloraxes(showscale=False)

        self.tree_fig.update_traces(
            textposition="middle center", selector=dict(type='treemap'))
        self.tree_fig.data[0].texttemplate = "%{label}<br>%{value}%"

        return self.tree_fig

    def grouped_bar_plot(self, comparision_object, comparision_group: str):
        '''Creates a grouped bar plot comparing curent class.object profile against other class.object profile  '''
        df_by_group = self.df[self.df['groups'] == comparision_group].sort_values(
            by='ratio', ascending=False).head(10)
        y_1 = df_by_group['ratio']
        x_1 = df_by_group['index'].str.capitalize()

        comparision_df1 = comparision_object.df[comparision_object.df['groups']
                                                == comparision_group]
        y_list = []
        for item in df_by_group['index']:
            new_y = comparision_df1[comparision_df1['index']
                                    == item]['ratio'].values[0]
            y_list.append(new_y)
        y_2 = y_list
        x_2 = x_1

        self.grouped_fig = go.Figure(data=[
            # Grouped bar principal plot
            go.Bar(
                name=f'<b>{str.capitalize(self.job)}</b>  Exp: <b>{self.experience}</b>  Degree: <b>{str.capitalize(self.degree)}</b>',
                x=y_1,
                y=x_1,
                marker=dict(
                    color=self.primary_color,
                ),
                text=y_1,
                textposition='inside',
                orientation='h',
                
            ),
            # Grouped bar secondary plot
            go.Bar(
                name=f'<b>{str.capitalize(comparision_object.job)}</b>  Exp: <b>{comparision_object.experience}</b>  Degree: <b>{str.capitalize(comparision_object.degree)}</b>',
                x=y_2,
                y=x_2,
                marker=dict(
                    color=self.secondary_color,
                ),
                text=y_2,
                textposition='inside',
                orientation='h',
                
            )
        ])

        self.grouped_fig.update_layout(
            barmode='group',
            # height=len(y_1) * 100,
        )

        # Title
        self.grouped_fig.update_layout(


            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                autorange="reversed",
                domain=[0, 0.95],
            ),
            xaxis=dict(
                domain=[0, 0.90],
            ),
            legend=dict(orientation="h",
                x=0.5,
                y=1.1, xanchor='center', yanchor="top"),
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor=self.background_color,
            plot_bgcolor=self.background_color,
        )

        return self.grouped_fig

    def most_demand_compare_barplot(self, comparision_object, comparision_group):
        '''Creates a grouped bar plot comparing curent class.object profile against other class.object profile  '''
        df_by_group = self.df[self.df['groups'] == comparision_group].sort_values(
            by='ratio', ascending=False).head(10)
        y_1 = df_by_group['ratio']
        x_1 = df_by_group['index'].str.capitalize()

        comparision_df2 = comparision_object.df[comparision_object.df['groups'] == comparision_group].sort_values(
            by='ratio', ascending=False).head(10)
        y_3 = comparision_df2['ratio']
        x_3 = comparision_df2['index'].str.capitalize()
        # Create two bar plots side by side to compare most in demand skills from each profile

        # Creating two subplots
        demand_comapre_fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                                           shared_yaxes=False,
                                           # vertical_spacing=0.0001
                                           )

        # Add bar chart for Profile 1
        demand_comapre_fig.add_trace(go.Bar(
            x=y_1,
            y=x_1,
            marker=dict(
                color=self.primary_color,
                line=dict(
                    color=self.primary_color,
                    width=1),
            ),
            name=f'<b>{str.capitalize(self.job)}</b>  Exp: <b>{self.experience}</b>  Degree: <b>{str.capitalize(self.degree)}</b>',
            text=y_1,
            textposition='inside',
            orientation='h',
        ), 1, 1)

        # Add bar chart for Profile 2
        demand_comapre_fig.add_trace(go.Bar(
            x=y_3,
            y=x_3,
            marker=dict(
                color=self.secondary_color,
                line=dict(
                    color=self.secondary_color,
                    width=1,)
            ),
            name=f'<b>{str.capitalize(comparision_object.job)}</b>  Exp: <b>{comparision_object.experience}</b>  Degree: <b>{str.capitalize(comparision_object.degree)}</b>',
            text=y_3,
            textposition='inside',
            orientation='h',
        ), 1, 2)

        # Title
        demand_comapre_fig.update_layout(
            # Axes
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                autorange="reversed",
                side='right',

                ticklabelposition="inside",

                # tickfont=dict(
                #     size=15,
                #     # color='rgba(102, 102, 102, 0.8)',
                #     # family=  "Droid Sans Mono",
                # ),
                domain=[0.05, 0.95],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                autorange="reversed",
                ticklabelposition="inside",
                # tickfont=dict(
                #     size=15,
                #     # color='rgba(102, 102, 102, 0.8)',
                #     # family=  "Droid Sans Mono",
                # ),
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0.05, 0.95],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=False,
                showgrid=True,
                autorange="reversed",
                domain=[0, 0.49],

            ),
            xaxis2=dict(
                zeroline=False,
                showline=False,
                showticklabels=False,
                showgrid=True,
                domain=[0.51, 1],
                # side='top',
                # dtick=25000,
            ),
            # showlegend=False,
            legend=dict(orientation="h",
                x=0.5,
                y=1.1, xanchor='center', yanchor="top"),
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor=self.background_color,
            plot_bgcolor=self.background_color,
            # showlegend=False,
        )

        # Annotations
        annotations = []
        # Adding percentage labels
        # for yd, y_3d, xd, x_3d in zip(y_1, y_3, x_1, x_3):
        #     # Percentage labels for Profile 1 plot
        #     annotations.append(dict(xref='x1', yref='y1',
        #                             y=xd, x=2,
        #                             text=str(yd) + '%',
        #                             font=dict(family='Arial', size=12,
        #                                       color='rgb(0, 0, 0)'),
        #                             showarrow=False))
        #     # Percentage labels for Profile 2 plot
        #     annotations.append(dict(xref='x2', yref='y2',
        #                             y=x_3d, x=2,
        #                             text=str(y_3d) + '%',
        #                             font=dict(family='Arial', size=12,
        #                                       color='rgb(0, 0, 0)'),
        #                             showarrow=False))
        # Footnotes
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.2, y=-0.109,
                                text='Figures are number of job posts a certain skills is mentioned in. As a percentage of total of the group',
                                font=dict(family='Arial', size=10,
                                          color='rgb(150,150,150)'),
                                showarrow=False))

        demand_comapre_fig.update_layout(annotations=annotations)

        return demand_comapre_fig


#job_profile1 =  JobFilter('analyst', '5+', 'phd',)
#job_profile2 = JobFilter('scientist', '5+', 'phd',)

# job_profile1.tree_map()
#compare_df = job_profile1.df_by_group('Skills')
# job_profile1.get_x()
#job_profile1.grouped_bar_plot(job_profile2, 'Skills')
#job_profile1.most_demand_compare_barplot(job_profile2 , 'Degree')
# job_profile1.df


# TEMP


    def bar_plot(self, comparision_group: str):
        '''Creates a grouped bar plot comparing curent class.object profile against other class.object profile  '''
        if comparision_group == 'all':
            df_by_group = self.df.sort_values(
                by='ratio', ascending=False).head(10)
            y_1 = df_by_group['ratio']
            x_1 = df_by_group['index'].str.capitalize()
        else:
            df_by_group = self.df[self.df['groups'] == comparision_group].sort_values(
                by='ratio', ascending=False).head(10)
            y_1 = df_by_group['ratio']
            x_1 = df_by_group['index'].str.capitalize()

        self.bar_fig = go.Figure(data=[
            # Grouped bar principal plot
            go.Bar(
                name=f'''Job: {self.job}
            Experience: {self.experience}
            Degree: {self.degree}''',
                x=y_1,
                y=x_1,
                marker=dict(
                    color=self.primary_color,
                ),
                text=y_1,
                textposition='inside',
                orientation='h'
            ),
        ])

        # Title
        self.bar_fig.update_layout(


            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                autorange="reversed",
                domain=[0, 0.95],
            ),
            xaxis=dict(
                domain=[0, 0.90],
            ),
            showlegend=False,
            # legend=dict(x=0.4, y=1.1, font_size=16, ),
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor=self.background_color,
            plot_bgcolor=self.background_color,
        )
        return self.bar_fig
