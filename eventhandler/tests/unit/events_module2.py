
def handler_from_module2():
    pass

HANDLERS = {
    'some_event': [handler_from_module2],
    'strange_event': [handler_from_module2],
    'tuple_event': (handler_from_module2,)
}
