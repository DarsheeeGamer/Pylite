from pylite.handler.ec import ErrorCode
class PyliteError(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self):
       return f"Error ({self.error_code}): {self.message}"
    

def handle_error(error, code = None):
    """Handles the error and stops the execution"""
    if isinstance(error, PyliteError):
       print(error)
       if code != None:
           print(f"Code: {code}")
    else:
        print(f"Unexpected Error: {error}")
    exit()
