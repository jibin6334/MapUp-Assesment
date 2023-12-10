import pandas as pd

def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = df.pivot_table(values='distance', index='id_start', columns='id_end', aggfunc='sum', fill_value=0)
    distance_matrix = distance_matrix + distance_matrix.T
    return distance_matrix
dataset_df = pd.read_csv('dataset-3.csv')
result_distance_matrix = calculate_distance_matrix(dataset_df)
print(result_distance_matrix)


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = df.reset_index().melt(id_vars='id_start', var_name='id_end', value_name='distance')
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled_df

distance_matrix_df = calculate_distance_matrix(dataset_df)
result_unrolled_df = unroll_distance_matrix(distance_matrix_df)
print(result_unrolled_df)



def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    filtered_df = df[
        (df['id_start'] != reference_id) &
        (df['distance'] >= (reference_avg_distance - threshold)) &
        (df['distance'] <= (reference_avg_distance + threshold))
    ]

    return filtered_df
unrolled_df = unroll_distance_matrix(distance_matrix_df)
result_filtered_df = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id=1001402)
print(result_filtered_df)



def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6
    return df
result_toll_rate_df = calculate_toll_rate(filtered_df)
print(result_toll_rate_df)



from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(df):
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    weekday_discounts = {
        (time(0, 0, 0), time(10, 0, 0)): 0.8,
        (time(10, 0, 0), time(18, 0, 0)): 1.2,
        (time(18, 0, 0), time(23, 59, 59)): 0.8,
    }
    weekend_discount = 0.7
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['start_day'] = df['timestamp'].dt.strftime('%A')
    df['start_time'] = df['timestamp'].dt.time
    df['end_day'] = df['start_day']
    df['end_time'] = df['start_time'] + timedelta(seconds=df['duration'])
    for index, row in df.iterrows():
        for time_range, discount_factor in weekday_discounts.items():
            if time_range[0] <= row['start_time'] <= time_range[1]:
                df.at[index, 'moto':'truck'] *= discount_factor
    df.loc[df['start_day'].isin(['Saturday', 'Sunday']), 'moto':'truck'] *= weekend_discount

    return df
result_time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rates_df)
print(result_time_based_toll_rates_df)

