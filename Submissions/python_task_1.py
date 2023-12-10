import pandas as pd

def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
   
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0

    return car_matrix
dataset_df = pd.read_csv('\dataset-1.csv')
result_car_matrix = generate_car_matrix(dataset_df)
print(result_car_matrix)


def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    type_counts = dict(sorted(type_counts.items()))

    return type_counts
dataset_df = pd.read_csv('dataset-1.csv')
result_type_counts = get_type_count(dataset_df)
print(result_type_counts)



def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    bus_indexes.sort()

    return bus_indexes
dataset_df = pd.read_csv('dataset-1.csv')
result_bus_indexes = get_bus_indexes(dataset_df)
print(result_bus_indexes)



def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    average_truck_per_route = df.groupby('route')['truck'].mean()
    filtered_routes = average_truck_per_route[average_truck_per_route > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes
dataset_df = pd.read_csv('dataset-1.csv')
result_filtered_routes = filter_routes(dataset_df)
print(result_filtered_routes)



def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)

    return modified_matrix
result_matrix = pd.DataFrame({
    'id_start': [10100, 10102, 10104],
    'id_end': [10102, 10104, 10106],
    'distance': [15.5, 22.8, 18.3]
})

result_modified_matrix = multiply_matrix(result_matrix)
print(result_modified_matrix)



def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    time_diff = df.groupby(['id', 'id_2']).apply(lambda group: group['end_timestamp'].max() - group['start_timestamp'].min())
    completeness_check = (
        (time_diff >= pd.Timedelta(days=1)) &
        (time_diff >= pd.Timedelta(days=7))     
    )
    return completeness_check
dataset_df = pd.read_csv('dataset-2.csv')
result_time_check = time_check(dataset_df)

print(result_time_check)
