import logging
import zmq

logging.basicConfig()
log = logging.getLogger("soundpicker-streamer")
log.setLevel(logging.INFO)

def main():

    log.info("Starting streaming device...")
    try:
        zmq_context = zmq.Context(1)
        # Socket facing clients
        zmq_frontend = zmq_context.socket(zmq.PULL)
        zmq_frontend.bind("tcp://*:5555")
        
        zmq_backend = zmq_context.socket(zmq.PUSH)
        zmq_backend.bind("tcp://*:5557")

        zmq.device(zmq.STREAMER, zmq_frontend, zmq_backend)
    except Exception as e:
        log.error(e)
    finally:
        pass
        zmq_frontend.close()
        zmq_backend.close()
        zmq_context.term()

if __name__ == "__main__":
    main()
