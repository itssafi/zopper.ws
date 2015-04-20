"""
Automated test module
"""

import unittest


class IntegrationTest(unittest.TestCase):

    def start_simple_wsgi_server(self):
        from pyramid.paster import get_app
        application = get_app('development.ini', 'main')
        from webtest import TestApp
        self.app = TestApp(application)
        return self.app


class TestDataLoad(IntegrationTest):

    def setUp(self):
        self.start_simple_wsgi_server()

    def test_data_load(self):
        """
        Test loading into database
        """
        DATA = """{"fields":[{"id":"a","label":"IMAGE INTENSIFICATION BASED DEVICES","type":"string"},{"id":"b","label":None,"type":"string"},{"id":"c","label":None,"type":"string"},{"id":"d","label":None,"type":"string"}],"data":[["DEVICE NAME","MGNIFICATION (X)","FIELD OF VIEW(degree)","RANGE(m)"],["Integrated Observation Equipment",7,7,2000],["Passive Night Vision Binocular (Mk-I)",4,10,500],["Passive Night Vision Goggles",1,40,225],["Passive Night Sight for 84 mm Carl",4,10,500],["Passive Night Sight for 5.56 mm Rifle",4,10,200],["Passive Night Sight for 5.56 mm LMG",4,10,200],["Passive Night Sight RCL Mk I",5,10,600],["Passive Night Sight RCL Mk II",6,9,600],["Driver Sight for T-55",1,40,100],["Gunners Night Sight for T-55",7,7,">800"],["Balloon Lifted Imaging & Surveillance","NA",2.1,4000],["Goggles for Aireforce",1,40,250],["Sight for 84 Mm",5.5,8,700]]}"""

        url = 'http://127.0.0.1:8080/dataload/'
        res = self.app.post(url, DATA, [('content-type','application/json')])
        assert res.status_int == 201


class TestSearchData(IntegrationTest):

    def setUp(self):
        self.start_simple_wsgi_server()

    def test_search_data(self):
        """
        Test data search using filter
        """
        url = 'http://127.0.0.1:8080/searchdata/?filter=field_of_view=7'
        res = self.app.get(url)
        assert res.status_int == 200
