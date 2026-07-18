# Integrated API Bridge

Small demo of a **REST to SOAP** bridge for a fake video-surveillance log API.

- **REST:** Flask (`app.py`) on port **5000**
- **SOAP:** spyne (`soap_server.py`) on port **8000**
- Optional: run both via the included `Dockerfile`

This is a teaching / integration sketch, not a production gateway.

## Requirements

```bash
pip install -r requirements.txt
```

## Run locally

Terminal 1 -- REST:

```bash
python app.py
```

Terminal 2 -- SOAP:

```bash
python soap_server.py
```

Or with Docker:

```bash
docker build -t integrated-api-bridge .
docker run --rm -p 5000:5000 -p 8000:8000 integrated-api-bridge
```

## REST examples

```bash
# All logs
curl -s http://127.0.0.1:5000/api/logs

# Logs for camera 1
curl -s http://127.0.0.1:5000/api/logs/1
```

## SOAP

- WSDL / service is served by spyne on port **8000** (see `soap_server.py`).
- Operation: `get_video_log(camera_id: int) -> string`

Example SOAP envelope (adjust host/path if your spyne bind differs):

```bash
curl -s -X POST http://127.0.0.1:8000 \
  -H "Content-Type: text/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="spyne.surveillance">
  <soap:Body>
    <tns:get_video_log>
      <tns:camera_id>1</tns:camera_id>
    </tns:get_video_log>
  </soap:Body>
</soap:Envelope>'
```

## License

MIT -- see [LICENSE](LICENSE).