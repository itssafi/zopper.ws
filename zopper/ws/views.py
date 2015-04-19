""" Cornice services."""

import logging
from cornice import Service
import json
import re

from schema import create_table, Zopper
from exceptions import (NoFilterPassed,
                        InvalidFilterFoundException)
from sqlalchemy import update
from sqlalchemy.sql import and_
from zopper.ws.dbkit import CreateSession, SessionCommit
from cornice.resource import resource


logger = logging.getLogger('zopper.ws')

# dataload = Service(name='dataload', path='/adddata', description="Load data")
# searchdata = Service(name='search', path='/search', description="Search data")
# status_dict = {}    


@resource(collection_path='/dataload/', path='/searchdata/')
class DataLoad(object):

    def __init__(self, request):
        self.request = request
        self.response_dict = {}
        self.session = CreateSession.createsession()
        logger.info("Initializing resources")
        logger.info("Requested URl: %s, HTTP Method Used: %s" % (self.request.url, self.request.method))
        logger.info("Module Name:'Views'")

    def collection_post(self):
        """
        Add data into database
        """
        dataload = self.request.body
        records = json.loads(dataload)
        data = records['data']
        fields = records['fields']
        columns = data.pop(0)
        for index, each_data in enumerate(data):
            values = Zopper(device_name=each_data[0],
                            gmnification=each_data[1],
                            field_of_view=each_data[2],
                            range=each_data[3])
            self.session.add(values)
            self.session.flush()
            logger.info('Loading record %s' % str(index+1))
        commit_obj = SessionCommit(self.session)
        commit_obj.commit(flag=True)
        self.session.close()
        self.response_dict['location'] = '/dataload/'
        self.response_dict['message'] = 'Data loaded successfully.'
        self.response_dict['status_code'] = 201
        return self.response_dict

    def get(self):
        """
        Search data from database
        """
        if self.request.GET:
            if not self.request.GET.has_key('filter'):
                msg = (400, "Filters must be passed with 'filter' in the URL")
                logger.exception("Filters must be passed with 'filter' in the URL."\
                                 "Error Status code:'%s' and Error Message:'%s'" % (msg[0], msg[1]))
                import pdb; pdb.set_trace()
                raise NoFilterPassed(msg)

            self.filter_str = self.request.GET.get('filter', '')
            search_results = self.filter_validation()
            logger.info("Fetching the query string passed.")
            common_query = self.session.query(Zopper.device_name,
                                              Zopper.gmnification,
                                              Zopper.field_of_view,
                                              Zopper.range)
            if search_results:
                logger.info("Passed query string:%s." % str(self.filter_str))
                results = common_query.filter(and_(*search_results)).all()

            if results:
                self.response_dict['location'] = '/searchdata/'
                self.response_dict['message'] = str(results)
                self.response_dict['status_code'] = 200
                return self.response_dict

            else:
                self.response_dict['location'] = '/searchdata/'
                self.response_dict['message'] = 'No data found'
                self.response_dict['status_code'] = 200
                return self.response_dict

    def filter_validation(self):
        """
        Validation of all the filter paramaters
        """
        filter_attributes = self.filter_str.split(',')
        terms = []
        for attribute in filter_attributes:
            filter_group = re.search(r'([a-zA-Z0-9_-]+)(=|==|>|<|<=|>=|!=)([a-zA-Z0-9_\-\.0-9]+)', attribute)
            if not filter_group:
                self.raise_invalid_filter_exception(attribute)

            key,operator,value = filter_group.groups()
            # Conversion from unicode to string
            value = str(value)

            if key == 'mgnification':
                #check_filter_operator_validity(operator, valid_opr=('='), passed_filter=attribute)
                expression = Zopper.mgnification == value

            elif key == 'field_of_view':
                #check_filter_operator_validity(operator, valid_opr=('='), passed_filter=attribute)
                expression = Zopper.field_of_view == value

            elif key == 'range':
                if operator == '==':
                    expression = Zopper.range == value
                elif operator == '>':
                    expression = Zopper.range > value
                elif operator == '<':
                    expression = Zopper.range < value
                elif operator == '>=':
                    expression = Zopper.range >= value
                elif operator == '<=':
                    expression = Zopper.range <= value
                else:
                    msg = (400, "The passed operator %s is invalid,"\
                           "the operator should be '==' or '>' or '>=' or '<='" % operator)
                    raise InvalidFilterFoundException(msg)

            else:
                self.raise_invalid_filter_exception(attribute)

            terms.append(expression)
        return terms

    def raise_invalid_filter_exception(self, passed_attribute):
        """
        Raise Exception when invalid filter is passed.
        """
        msg = (400, "'{0}' is an invalid filter."\
               " These are the valid filters and their corresponding operators to be used: "\
               "(1)Filter:'mgnification', Operators:'=' "\
               "(2)Filter:'field_of_view' Operators:'=' "\
               "(3)Filter:'range' Operators:'==,>,<,<=,>=' "\
               "like '?filter=gmnification=7' or '?filter=range>=800&field_of_view=8'."
               "Kindly pass the valid filter with their corresponding operator and try again.".format(passed_attribute.strip('"')))
        logger.exception("Invalid Filter Passed. Error Status code:'%s' and Error Message:'%s'" % (msg[0], msg[1]))
        raise InvalidFilterFoundException(msg)
