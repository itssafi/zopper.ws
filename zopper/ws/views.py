""" Cornice services."""

import logging
from cornice import Service
import json
import re

from schema import create_table, Zopper
from exceptions import (NoFilterPassed,
                        InvadilDataException,
                        InvalidFilterFoundException,
                        NoDataPassedException)
from sqlalchemy import update
from sqlalchemy.sql import and_
from zopper.ws.dbkit import CreateSession, SessionCommit
from cornice.resource import resource
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


logger = logging.getLogger('zopper.ws')
config = ConfigParser()
config.read('zopper.ws//development.ini')
should_commit = json.loads(config.get('zopper_config', 'commit'))


@resource(collection_path='/dataload/', path='/searchdata/')
class DataLoad(object):

    def __init__(self, request):
        self.request = request
        self.response_dict = {}
        self.session = CreateSession.createsession()
        logger.info("Initializing resources")
        logger.info("Requested URl: %s,"\
                    " HTTP Method Used: %s" % (self.request.url,
                                               self.request.method))
        logger.info("Module Name:'Views'")

    def collection_post(self):
        """
        Add data into database
        """
        try:
            dataload = self.request.body
            records = json.loads(dataload)
            data = records['data']
            fields = records['fields']
            columns = data.pop(0)
            if not data:
                msg = (400, "No data passed in payload: %s" % (dataload))
                return NoDataPassedException(msg)

            for index, each_data in enumerate(data):
                values = Zopper(device_name=each_data[0],
                                mgnification=each_data[1],
                                field_of_view=each_data[2],
                                range=each_data[3])
                self.session.add(values)
                self.session.flush()
                logger.info('Loading record %s' % str(index+1))

            commit_obj = SessionCommit(self.session)
            commit_obj.commit(flag=should_commit)
            self.session.close()
            response_msg = {"response_msg": 'Data loaded successfully.'}
            self.response_dict['location'] = '/dataload/'
            self.response_dict['message'] = str(response_msg)
            self.response_dict['status_code'] = 201
            return self.response_dict
        except Exception:
            msg = (400, "Invalid data passed in payload: %s" % (dataload))
            return InvadilDataException(msg)

    def get(self):  
        """
        Search data from database
        """
        if self.request.GET:
            if not self.request.GET.has_key('filter'):
                msg = (400, "Filters must be passed with 'filter' in the URL")
                logger.exception("Filters must be passed with 'filter' in the URL."\
                                 "Error Status code:'%s' and Error Message:'%s'" % (msg[0], msg[1]))
                return NoFilterPassed(msg)

            self.filter_str = self.request.GET.get('filter', '')
            search_results = self.filter_validation()

            if not search_results[1]:
                msg = (400, "'{0}' is an invalid filter."\
                           " These are the valid filters and their corresponding operators to be used: "\
                           "(1)Filter:'mgnification', Operators:'=' "\
                           "(2)Filter:'field_of_view' Operators:'=' "\
                           "(3)Filter:'range' Operators:'=' "\
                           "like '?filter=gmnification=7' or '?filter=range=800&field_of_view=8'."\
                           "Kindly pass the valid filter with their corresponding "\
                           "operator and try again.".format(search_results[0].strip('"')))
                return InvalidFilterFoundException(msg)

            logger.info("Fetching the query string passed.")
            common_query = self.session.query(Zopper.device_name,
                                              Zopper.mgnification,
                                              Zopper.field_of_view,
                                              Zopper.range)
            if search_results[0]:
                logger.info("Passed query string:%s." % str(self.filter_str))
                results = common_query.filter(and_(*search_results[0])).all()
                self.session.close()

            res = []
            if results:
                for index, value in enumerate(results):
                    row_data = {}
                    row_data = {"DEVICE_NAME": value[0],
                                "MGNIFICATION": value[1],
                                "FIELD_OF_VIEW": value[2],
                                "RANGE": value[3]}
                    res.append(row_data)

            self.response_dict['location'] = '/searchdata/'
            self.response_dict['message'] = str({"SearchData": res})
            self.response_dict['status_code'] = 200
            if not res:
                logger.info("No recond found !!!")
                self.response_dict['status_code'] = 404
            self.session.close()
            return self.response_dict

    def filter_validation(self):
        """
        Validation of all the filter paramaters
        """
        filter_attributes = self.filter_str.split(',')
        terms = []
        for attribute in filter_attributes:
            filter_group = re.search(r'([a-zA-Z0-9_-]+)(=)([a-zA-Z0-9_\-\.0-9]+)', attribute)
            if not filter_group:
                return (attribute, False)

            key,operator,value = filter_group.groups()
            # Conversion from unicode to string
            value = str(value)

            if key == 'mgnification':
                expression = Zopper.mgnification == value

            elif key == 'field_of_view':
                expression = Zopper.field_of_view == value

            elif key == 'range':
                expression = Zopper.range == value

            else:
                return (attribute, False)

            terms.append(expression)
        return (terms, True)
