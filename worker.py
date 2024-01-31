from spleeter.separator import Separator

import logging
import zmq

logging.basicConfig()
log = logging.getLogger("soundpicker-worker")
log.setLevel(logging.INFO)

def process(source_file, target_dir, separator_type):
    separator = separators[separator_type]
    separator.separate_to_file(source_file, target_dir)

    with open(f"{target_dir}/SUCCESS", "w") as f:
        pass


def worker():
    log.info("Initializing receiver...")

    zmq_context = zmq.Context()
    zmq_receiver = zmq_context.socket(zmq.PULL)
    zmq_receiver.connect("tcp://127.0.0.1:5557")

    while True:
        payload = zmq_receiver.recv_json()
        log.info(f"Received request: {payload}")
        process(payload['source_file'], payload['target_dir'], payload['split_type'])       

if __name__ == '__main__':
    global separators

    log.info("Initializing separators...")
    separators = {}
    separators['spleeter:2stems'] = Separator('spleeter:2stems')
    separators['spleeter:4stems'] = Separator('spleeter:4stems')
    separators['spleeter:5stems'] = Separator('spleeter:5stems')
    
    worker()

