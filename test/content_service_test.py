# -*- coding: utf-8 -*-

import os
import io
import tarfile

from betamax import Betamax
from requests import Session
from nose.tools import assert_equal, assert_true, assert_false, assert_in

from . import URL, APIKEY
from submitter.content_service import ContentService

class TestContentService():

    def setup(self):
        session = Session()
        self.betamax = Betamax(session)
        self.cs = ContentService(url=URL, apikey=APIKEY, session=session)

    def test_checkassets(self):
        # curl -X POST -H "Authorization: deconst ${APIKEY}" \
        #   http://dockerdev:9000/assets \
        #   -F aaa=@test/fixtures/assets/foo/aaa.jpg \
        #   -F bbb=@test/fixtures/assets/bar/bbb.gif

        with self.betamax.use_cassette('checkassets'):
            response = self.cs.checkassets({
                'foo/aaa.jpg': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'bar/bbb.gif': '8810ad581e59f2bc3928b261707a71308f7e139eb04820366dc4d5c18d980225',
                'baz/missing.css': 'ffa63583dfa6706b87d284b86b0d693a161e4840aad2c5cf6b5d27c3b9621f7d'
            })

            assert_equal(response, {
                'foo/aaa.jpg': '/__local_asset__/aaa-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.jpg',
                'bar/bbb.gif': None,
                'baz/missing.css': None
            })

    def test_bulkasset(self):
        with self.betamax.use_cassette('bulkasset'):
            tarball = io.BytesIO()
            tf = tarfile.open(fileobj=tarball, mode='w:gz')

            entry0 = tarfile.TarInfo('bar/bbb.gif')
            entry0.size = 0
            tf.addfile(entry0, io.BytesIO())

            entry1 = tarfile.TarInfo('foo/aaa.jpg')
            entry1.size = 0
            tf.addfile(entry1, io.BytesIO())

            tf.close()

            response = self.cs.bulkasset(tarball.getvalue())

            assert_equal(response, {
                'bar/bbb.gif': '/__local_asset__/bbb-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.gif',
                'foo/aaa.jpg': '/__local_asset__/aaa-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.jpg'
            })