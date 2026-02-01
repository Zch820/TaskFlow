from rest_framework.views import exception_handler


def simple_error_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            message = response.data.get("detail")
        else:
            message = str(response.data)
        response.data = {"error": str(message)}

    return response
