from flask import current_app

def print_debug(message):
    """
    Prints a message only when app is in debug mode
    @param message : message to print
    """
    if current_app.config['DEBUG']:
        print(message)
