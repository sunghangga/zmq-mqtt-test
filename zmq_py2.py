from gzip import GzipFile
from cStringIO import StringIO
import zmq
import xmltodict, json
import xml.etree.ElementTree as ET

context = zmq.Context()

subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7658")
subscriber.setsockopt(zmq.SUBSCRIBE, "/RIG/KV6posinfo")
subscriber.setsockopt(zmq.SUBSCRIBE, "/RIG/KV17cvlinfo")

while True:
    multipart = subscriber.recv_multipart()
    address = multipart[0]
    contents = ''.join(multipart[1:])
    try:
        contents = GzipFile('','r',0,StringIO(contents)).read()
        # print('GZIP', address, contents)
        # xml = xmltodict.parse(contents)
        # print(xml)
        # print(json.dumps(xml))

        print(contents)
        # root = ET.fromstring(contents)
        # print(root)
        # for value in root.iter('tmi8:vehiclenumber'):
        #     print(value.text)

    except:
        raise
        print('NOT ', address, contents)

subscriber.close()
context.term()