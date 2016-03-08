def handler_from_module1():
    pass


def other_handler_from_module1():
    pass


HANDLERS = {
    'some_event': [handler_from_module1, other_handler_from_module1],
    'other_event': [other_handler_from_module1]
}
