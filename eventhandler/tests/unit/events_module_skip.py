def skip_method():
    pass

HANDLERS = {
    'skip_direct_call': skip_method,
    'skip_usage_of_dict': {'method1': skip_method},
    'skip_string': 'skip_method',
    'skip_list_of_string': ['skip_method']
}
