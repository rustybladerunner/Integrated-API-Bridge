# REST and SOAP examples

Two small Python services return synthetic camera-event data. They demonstrate
JSON over REST and XML over SOAP. Despite the repository name, **there is no
REST-to-SOAP forwarding layer**: each service uses its own sample records.

This is an educational experiment, not a production gateway. It has no
authentication, encryption, persistent storage, or real camera integration.
SOAP does not enable WS-Security automatically; this example does not implement it.

## Tested setup

Use **Python 3.11**. The maintenance check used Python 3.11.16, Flask 3.1.3,
Spyne 2.14.0, and lxml 6.1.3. Spyne failed to import on Python 3.12 in this review.
Newer Python versions are not supported by this setup.

Create and activate a virtual environment, then install the resolved dependencies:

```sh
python -m venv .venv
# Windows PowerShell: .venv/Scripts/Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.lock
```

`requirements.txt` lists direct dependencies; `requirements.lock` also pins their
dependencies. Recheck the tests when updating either file.

## Run locally

In one terminal, run `python app.py`. In another, run `python soap_server.py`.
Both bind to `127.0.0.1`, and the Flask debugger is off. Stop them with Ctrl+C.
The local servers are for experiments; do not expose them to an untrusted network.

The old Dockerfile remains a historical example. It is not a supported launch
path for this revision: it uses a different Python version, and these loopback
bindings do not provide the old published-port behavior. Use the tested local setup.

## REST

```sh
curl http://127.0.0.1:5000/api/logs
curl http://127.0.0.1:5000/api/logs/1
```

An unknown camera returns an empty JSON array.

## SOAP

The WSDL is available at `http://127.0.0.1:8000/?wsdl`.
Send this XML as an HTTP POST to `http://127.0.0.1:8000/` with
`Content-Type: text/xml; charset=utf-8`:

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="spyne.surveillance">
  <soap:Body>
    <tns:get_video_log><tns:camera_id>1</tns:camera_id></tns:get_video_log>
  </soap:Body>
</soap:Envelope>
```

The response includes `Motion detected at 10:00:00`. An unknown camera returns
`No log for this camera`. Malformed XML produces a SOAP fault.

## Checks

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests send real HTTP requests to temporary loopback servers, check known and
unknown camera responses and malformed XML, and verify launcher defaults.
They do not establish production security or external-service compatibility.

## License

MIT — see [LICENSE](LICENSE).
