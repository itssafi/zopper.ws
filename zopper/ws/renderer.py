import logging
from pyramid.response import Response
from pyramid.response import response_adapter
logger = logging.getLogger('zopper.ws')


@response_adapter(dict)
def dict_response(response_dict):
    """ Generating response out of the dictionary responder output. """
    #import pdb;pdb.set_trace()
    headerlist = []
    if response_dict.has_key('location'):
        logger.info("Passing the location of the generated resource.")
        headerlist.append(('location', response_dict['location']))

    logger.info("Successfully generated response.")

    return Response(content_type='application/json',
                    status_int = response_dict['status_code'],
                    body = response_dict['message'],
                    headerlist = headerlist
                    )


@response_adapter(Exception)
def exception_response(exception):
    """ Generating a response when a exception is raised. """
    status_code = 500
    exception_message = str(exception)

    if hasattr(exception,'value'):
        status_code = exception.status_code
        exception_message = {"WebServiceError": {"exception_class": exception.__class__.__name__,
                                                 "message": exception.value, "log_level": "ERROR"}}
        logger.info("Generated exception status_code: '%s' and JSON:'%s'." % (exception.status_code, exception_message))
    else:
        exception_message = {"WebServiceError": {"error": exception.message}}
        logger.info("Generated exception JSON:'%s'." % (exception_message))

    return Response(content_type='application/json',
                    body=str(exception_message),
                    status_int = status_code)
