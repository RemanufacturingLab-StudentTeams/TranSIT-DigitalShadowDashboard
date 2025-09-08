import pandas as pd


def filter_timestamps(df, time_dict):
    start, stop = time_dict['start'], time_dict['stop']
    start_dt, stop_dt = timestamp_to_datetime(start), timestamp_to_datetime(stop)
    filtered_df = df[df['datetime'].apply(lambda v: in_range(v, start_dt, stop_dt))]
    return filtered_df


def timestamp_to_datetime(timestamp):
    dt = pd.to_datetime(timestamp)
    dt_tz = dt.tz_localize('UTC')
    return dt_tz


def in_range(timestamp, start=None, stop=None):
    return (start is None or timestamp >= start) and (stop is None or timestamp <= stop)
