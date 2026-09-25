from contextlib import contextmanager
import runpy
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from unittest.mock import Mock
from wsgiref.simple_server import make_server
import json
import xml.etree.ElementTree as ET
import pytest
from app import app
from soap_server import wsgi_application

@contextmanager
def serving(application):
    server = make_server('127.0.0.1', 0, application)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

def test_rest_returns_sample_data_and_empty_unknown_camera():
    with serving(app) as url:
        with urlopen(url+'/api/logs', timeout=3) as response:
            assert len(json.load(response)) == 2
        with urlopen(url+'/api/logs/1', timeout=3) as response:
            assert json.load(response)[0]['event'] == 'motion detected'
        with urlopen(url+'/api/logs/999', timeout=3) as response:
            assert json.load(response) == []

@pytest.mark.parametrize('camera,expected', [(1,'Motion detected at 10:00:00'),(999,'No log for this camera')])
def test_soap_round_trip(camera, expected):
    envelope = f'''<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:t="spyne.surveillance">
      <soap:Body><t:get_video_log><t:camera_id>{camera}</t:camera_id></t:get_video_log></soap:Body></soap:Envelope>'''.encode()
    with serving(wsgi_application) as url:
        request = Request(url, data=envelope, headers={'Content-Type':'text/xml; charset=utf-8'})
        with urlopen(request, timeout=3) as response:
            tree = ET.fromstring(response.read())
            assert tree.find('.//{spyne.surveillance}get_video_logResult').text == expected

def test_soap_rejects_malformed_xml():
    with serving(wsgi_application) as url:
        with pytest.raises(HTTPError) as error:
            urlopen(Request(url, data=b'<broken', headers={'Content-Type':'text/xml'}), timeout=3)
        assert error.value.code in (400, 500)

def test_rest_launcher_is_loopback_without_debugger(monkeypatch):
    run = Mock()
    monkeypatch.setattr('flask.Flask.run', run)
    runpy.run_path('app.py', run_name='__main__')
    assert run.call_args.kwargs['host'] == '127.0.0.1'
    assert run.call_args.kwargs['debug'] is False

def test_soap_launcher_is_loopback(monkeypatch):
    factory = Mock()
    monkeypatch.setattr('wsgiref.simple_server.make_server', factory)
    runpy.run_path('soap_server.py', run_name='__main__')
    assert factory.call_args.args[:2] == ('127.0.0.1', 8000)
