# SOAP is a protocol for exchanging structured information in the implementation of web services. 
# It is highly standardized and uses XML for message formatting. 
# SOAP works over several application layer protocols, such as HTTP, SMTP, and more.
# 
# Data format: SOAP exclusively uses XML for message transmission.
# 
# Strict and Robust: SOAP has built-in error handling and security features like WS-Security, 
# which makes it ideal for applications that require strict standards and security measures.

# Benefits for Video Management Systems (VMS):
# Security and Reliability: SOAP’s built-in features like WS-Security ensure secure video data transmission between clients and servers, 
# which is essential in sensitive environments like airports or financial institutions.
#
# Standardized Protocol: SOAP is often used in enterprise-level applications where strict protocols need to be followed, 
# such as when integrating VMS with government systems or third-party enterprise tools.
#
# Complex Operations: SOAP allows for more complex operations in the video management system, 
# such as triggering specific camera actions (e.g., pan, tilt, zoom), requesting stored footage, or starting/stopping recordings.
#
# Transactional: SOAP is designed to handle complex transactions, making it suitable for environments where precise interactions 
# (such as event triggers and alarm systems) are necessary for handling video data.

########################################

#import necessary modules
#spyne: A Python library for building RPC (Remote Procedure Call) services, including SOAP (Simple Object Access Protocol).
# Application: Represents a Spyne application that ties services and protocols together.
# rpc: A decorator that turns methods into remote procedure calls.
# ServiceBase: A base class for creating service classes.
# Integer and Unicode: Data types used for request and response parameters (similar to defining types in function arguments).
# Soap11: The protocol used for SOAP 1.1.
# WsgiApplication: A WSGI application wrapper to handle requests and responses.
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Define a service class.
# SurveillanceService: A class inheriting from ServiceBase, which defines our SOAP service. This class will hold all the methods (operations) for our SOAP API.
# @rpc(Integer, _returns=Unicode): Decorates the get_video_log() function as an RPC method. It accepts an Integer (camera_id) as input and returns a Unicode string.
# The method looks up the log for the given camera_id in the logs dictionary.
class SurveillanceService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_video_log(ctx, camera_id):
        logs = {
            1: "Motion detected at 10:00:00",
            2: "No motion at 10:15:00"
        }
        return logs.get(camera_id, "No log for this camera")

# Create the SOAP application.
# Application: Combines the SurveillanceService with the SOAP protocol.
# tns='spyne.surveillance': Defines the "target namespace" (a unique identifier for the service).
# in_protocol and out_protocol: Specify that the service will use SOAP 1.1 for both input and output, validated by the lxml library.
# WsgiApplication: Wraps the application in a WSGI app, making it compatible with Python's WSGI web servers.
application = Application([SurveillanceService], tns='spyne.surveillance',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

# Run the SOAP server
#
# make_server('0.0.0.0', 8000, wsgi_application): This creates an HTTP server that 
# listens on all available network interfaces (0.0.0.0) and port 8000, 
# and it uses the wsgi_application to handle requests.
#
# server.serve_forever(): Starts the server and listens for incoming requests indefinitely.
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("SOAP server is running on http://localhost:8000")
    server.serve_forever()

