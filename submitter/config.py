# -*- coding: utf-8 -*-

class Config:
    """
    Load configuration values from the environment.
    """

    def __init__(self, env):
        self.envelope_dir = env.get('ENVELOPE_DIR')
        self.asset_dir = env.get('ASSET_DIR')
        self.content_service_url = env.get('CONTENT_SERVICE_URL')
        self.content_service_apikey = env.get('CONTENT_SERVICE_APIKEY')

        if self.content_service_url.endswith('/'):
            self.content_service_url = self.content_service_url[:-1]

    def missing(self):
        m = []
        if not self.envelope_dir:
            m.append('ENVELOPE_DIR')
        if not self.asset_dir:
            m.append('ASSET_DIR')
        if not self.content_service_url:
            m.append('CONTENT_SERVICE_URL')
        if not self.content_service_apikey:
            m.append('CONTENT_SERVICE_APIKEY')
        return m

    def is_valid(self):
        return not self.missing()