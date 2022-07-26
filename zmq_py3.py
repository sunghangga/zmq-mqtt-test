from gzip import GzipFile
from io import BytesIO
import zmq
import xmltodict, json

context = zmq.Context()

subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7658")
subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV6posinfo")
subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV17cvlinfo")

while True:
    multipart = subscriber.recv_multipart()
    address = multipart[0]
    contents = b''.join(multipart[1:])
    try:
        contents = GzipFile('','r',0,BytesIO(contents)).read()
        # print('GZIP', address, contents)
        xml = xmltodict.parse(contents.decode("utf-8"))
        print(json.dumps(xml))
    except:
        raise
        print('NOT ', address, contents)

subscriber.close()
context.term()