# Filters out specified partitions from partition data
def filter_partitions(partition_data, filter_list):
    for filter in filter_list:
        if filter in partition_data:
            del partition_data[filter]
