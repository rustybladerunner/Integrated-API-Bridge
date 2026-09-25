"""Independent SOAP teaching example; no authentication or WS-Security."""
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class SurveillanceService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_video_log(ctx, camera_id):
        logs = {1: "Motion detected at 10:00:00", 2: "No motion at 10:15:00"}
        return logs.get(camera_id, "No log for this camera")

application = Application(
    [SurveillanceService], tns='spyne.surveillance',
    in_protocol=Soap11(validator='lxml'), out_protocol=Soap11(),
)
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("SOAP demo is running on http://127.0.0.1:8000")
    server.serve_forever()
