""" Cornice services."""

import logging
from cornice import Service
import json

from schema import create_table
from exceptions import SourceDestinationSameError, KeyMissingError, ValueMissingError
from sqlalchemy import update
from zopper.ws.dbkit import CreateSession, SessionCommit


logger = logging.getLogger('zopper.ws')

dataload = Service(name='dataload', path='/adddata', description="A application for searching/filtering the data set")


class DataLoad(object):

    def __init__(self):
        self.status_dict = {}

    @dataload.post()
    def add_bus_route(request):
        """
        Add data into database
        """
        bus_info = request.body
        records = json.loads(bus_info)
        import pdb; pdb.set_trace()
        status_dict['status_msg'] = str(records)
        route_no = records['route_no']
        source = records['source']
        destn = records['destn']
        seats = int(records['seats'])
        route[route_no] = [source, destn]
        values = Bus(route_no=route_no, source=source, destn=destn, seats=seats)

        session = CreateSession.createsession()
        session.add(values)
        session.flush()
        commit_obj = SessionCommit(session)
        commit_obj.commit(flag=True)
        session.close()
        status_dict['location'] = '/dataload'
        status_dict['status_code'] = 200
        return status_dict
