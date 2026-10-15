import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PresentationApiMountTests(unittest.TestCase):
    def test_browser_request_stays_beneath_the_presentation_mount(self):
        source = (ROOT / 'src/live/demoAdapter.ts').read_text()
        self.assertIn("url: './api/v1/qualifications'", source)
        self.assertNotIn("url: '/api/v1/qualifications'", source)

    def test_presentation_proxies_only_its_qualification_api(self):
        config = (ROOT / 'nginx.conf').read_text()
        self.assertIn('location /api/v1/qualifications', config)
        self.assertIn('proxy_pass http://virtualization-ai-501-qualification-adapter:8080;', config)
        self.assertNotIn('proxy_ssl_verify off', config)
