import numpy as np
import pandas as pd
from datetime import timedelta, datetime
from dateutil import parser

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)


def process_map_data(df, df_positions, scatter_graph_config, df_location):
    return (df
            .pipe(add_location_properties, df_positions, df_location)
            .pipe(timestamps_to_datetimes)
            .pipe(add_record_count)
            .pipe(add_marker_size, scatter_graph_config)
            .pipe(filter_by_arg, scatter_graph_config)
            .pipe(get_time_spent)
            .pipe(average_time_spent)
            .pipe(add_hover_text, scatter_graph_config)
            .pipe(group_by_column, scatter_graph_config))


def add_location_properties(df, df_pos, df_loc):
    df_loc = df_loc.rename(columns={"id": "sublocationId"})
    df_loc = df_loc.rename(columns={"name": "Sublocation Name"})

    df = df.merge(df_loc[['sublocationId',
                          'Sublocation Name']],
                  on=['Sublocation Name'],
                  how='inner'
                  )

    df_pos = df_pos.rename(columns={"associated_status": "status"})
    df_pos = df_pos.rename(columns={"department": "location"})
    df_pos = df_pos.rename(columns={"name": "Sublocation Name"})
    df["Operation"] = df["status"].str.removesuffix(" - Done").str.removesuffix(" - Pause")
    df["is_waiting"] = df["status"].str.endswith((" - Done", " - Pause"))
    combined_df = df.merge(df_pos[['Sublocation Name',
                                   'X_coord',
                                   'Y_coord',
                                   ]],
                           on=['Sublocation Name'],
                           how='inner')
    print(combined_df)
    return combined_df


def timestamps_to_datetimes(df):
    df['datetime'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    return df


def add_record_count(df):
    locations_counted = df.groupby(['Sublocation Name']).size().reset_index(name='count')
    df_counted = df.merge(locations_counted, on=['Sublocation Name'])
    return df_counted


def compare_averages(df, scatter_graph_config):
    if scatter_graph_config.get('calculate_averages'):
        return (df.pipe(add_mean_time)
                  .pipe(compare_mean_to_norm)
                  .pipe(get_mean_over_norm))
    else:
        return df


def add_mean_time(df):
    locations_averaged = df.groupby(['Location_ID'])['Process_time'].mean().reset_index(name='Average process time')
    locations_averaged['Average process time'] = locations_averaged['Average process time'].dt.round('1s')
    df_averaged = df.merge(locations_averaged, on=['Location_ID'])
    return df_averaged


def compare_mean_to_norm(df):
    df['Norm_time_delta'] = df['Norm_time (seconds)'].apply(lambda x: timedelta(seconds=x))
    df['Average-Norm'] = df.apply(lambda row: row['Average process time']-row['Norm_time_delta'], axis=1)
    df['Average-Norm-Numeric'] = df['Average-Norm'].dt.total_seconds()
    return df


def get_mean_over_norm(df):
    df['difference/norm'] = df.apply(lambda row: row['Average-Norm-Numeric'] / row['Norm_time (seconds)'], axis=1)
    df['difference/norm'] = df['difference/norm'].round(decimals=2)
    df['difference/norm_percentage'] = df.apply(lambda row: f"{row['difference/norm']*100}%", axis=1)
    return df


def add_hover_text(df_counted, scatter_graph_config):
    hover_text_type = scatter_graph_config.get('hover_text_type')
    if hover_text_type == 'many':
        df_labelled = add_many_hover_text(df_counted)
    elif hover_text_type == 'single':
        df_labelled = add_single_hover_text(df_counted)
    elif hover_text_type == 'status':
        df_labelled = add_status_hover_text(df_counted)
    elif hover_text_type == 'averages':
        df_labelled = add_averages_hover_text(df_counted)
    else:
        df_labelled = add_empty_hover_text(df_counted)
    return df_labelled


def add_single_hover_text(df_counted):

    df_counted['hover_text'] = df_counted.apply(

        lambda row: f"Part ID: {row['id']}<br>"
                    f"Timestamp: {row['Timestamp']}<br>"
                    f"Reported status: {row['status']}<br>"
                    f"Sub-location: {row['Sublocation Name']}<br>", axis=1
    )

    return df_counted


def add_many_hover_text(df_counted):

    hover_text = df_counted.groupby(['status']).apply(
        lambda group: '<br>'.join(
            f"Part ID: {row['id']}<br>"
            f"Timestamp: {row['Timestamp']}<br>"
            f"Reported status: {row['status']}<br>"
            f"Sub-location: {row['Sublocation Name']}<br>"
            for _, row in group.iterrows()
        )
    ).reset_index(name='hover_text')

    df_hover = df_counted.merge(hover_text, on=['status'])
    return df_hover


def add_status_hover_text(df_counted):

    hover_text = df_counted.groupby(['Location_ID']).apply(
        lambda group: '<br>'.join(
            f"Part ID: {row['id']}<br>"
            f"Timestamp: {row['Timestamp']}<br>"
            f"Reported status: {row['status']}<br>"
            f"Sub-location: {row['Sublocation Name']}<br>"
            for _, row in group.iterrows()
        )
    ).reset_index(name='status')

    df_hover = df_counted.merge(hover_text, on=['Location_ID'])
    return df_hover


def add_averages_hover_text(df):

    df['hover_text'] = df.apply(

        lambda row: f"Sub-location: {row['Sublocation Name']}<br>"
                    f"Average time spent: {row['average_time_spent']} seconds<br>",
        axis=1
    )
    return df


def add_empty_hover_text(df_counted):
    df_counted['hover_text'] = df_counted.apply(
        lambda row: '',
        axis=1
    )
    return df_counted


def add_marker_size(df_counted, scatter_graph_config):
    if scatter_graph_config.get('marker_size') is None:
        # adjust marker size based on the number of records
        df_counted['marker_size'] = df_counted['count'] * 8
        # add max limit
        max_marker_size = 60
        df_counted['marker_size'] = np.clip(df_counted['marker_size'], None, max_marker_size)
        return df_counted
    else:
        return df_counted


def filter_by_arg(df, scatter_graph_config):
    if scatter_graph_config.get('filter_by'):
        df_grouped = group_by_column(df, scatter_graph_config)
        df_filtered = df_grouped.filter(
            lambda x: x[scatter_graph_config['filter_by']].iloc[0] in scatter_graph_config['important_statuses'])
        return df_filtered
    else:
        return df


def get_time_spent(df):
    df = df.sort_values(by=['Timestamp'], ascending=True)
    df = df.groupby('id')
    modified_groups = []
    for group_name, data in df:
        data["next_timestamp"] = data["Timestamp"].shift(-1)
        data["time_spent"] = data["next_timestamp"] - data["Timestamp"]
        modified_groups.append(data)

    df = pd.concat(modified_groups)
    return df


def average_time_spent(df):
    locations_averaged = df.groupby(['Sublocation Name'])["time_spent"].mean().reset_index(name='average_time_spent')
    locations_averaged['average_time_spent'] = locations_averaged['average_time_spent'].dt.round('1s')
    df_averaged = df.merge(locations_averaged, on=['Sublocation Name'])
    df_averaged['average_in_hours'] = df_averaged['average_time_spent'].dt.total_seconds()/3600
    return df_averaged


def group_by_column(df, scatter_graph_config):
    df = df.sort_values(by=['Timestamp'], ascending=True)
    if scatter_graph_config.get('group_by'):
        grouped_df = df.groupby(scatter_graph_config['group_by'])
        return grouped_df
    else:
        return df
