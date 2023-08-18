from rest_framework.response import Response
import inspect


def catch_exceptions(func):
    """
    Decorator to catch exceptions and return a json response with the error message and
    a flag to indicate that the request was (not) successful.
    """
    def wrapper(request, *args, **kwargs) -> Response:
        try:
            response = func(request, *args, **kwargs)  # Call the view function which ALWAYS returns a dict
            response['success'] = True
        except Exception as e:
            callerFrameRecord = inspect.stack()[1]
            callerFrame = callerFrameRecord[0]
            info = inspect.getframeinfo(callerFrame)
            message = f'Exception in {info.filename}  in {info.function} at line {info.lineno}: {str(e)}'
            print('===========================================================================================\n')
            print(message)
            print('\n===========================================================================================')
            response = {'success': False, 'exception': str(e), 'message': message}
        return Response(response)
    return wrapper