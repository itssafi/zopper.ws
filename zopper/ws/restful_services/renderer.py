import logging
from pyramid.response import Response
from pyramid.response import response_adapter

logger = logging.getLogger('zopper.ws')

@response_adapter(dict)
def dict_response(status_dict):
    """ Generating response out of the dictionary responder output. """
    #import pdb;pdb.set_trace()
    headerlist = []
    if status_dict.has_key('location'):
        logger.info("Passing the location of the generated resource.")
        headerlist.append(('location', status_dict['location']))

    logger.info("Successfully generated response.")

    return Response(content_type='application/plain',
                    status_int = status_dict['status_code'],
                    body = status_dict['status_msg'],
                    headerlist = headerlist
                    )

@response_adapter(Exception)
def exception_response(exception):
    """ Generating a response when a exception is raised. """
    #import pdb;pdb.set_trace()
    status_int = 400
    exception_message = str(exception)

    return Response(content_type='application/plain',
                    body=exception_message,
                    status_int = status_int
                   )
