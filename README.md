# SoundPicker 
## About
**SoundPicker** is designed to work with audio files and use already trained state of the art models for performing separations and variouse sound extractions. The current version tests Spleeter a source separation library with pretrained models written in Python and uses Tensorflow. This implementation includes Vocals / accompaniment separation API usage. 

## Running
### Launching ZeroMQ Message Streamer
```bash
python3 streamer_device.py
```

### Launching Worker (ZeroMQ Consumer)
To launch workers the below command needs to be executes one or multiple times:
```bash
python3 worker.py
```

### Launching REST API (ZeroMQ Publisher)
```bash
gunicorn --timeout 120 --bind 127.0.0.1:8080 wsgi:app
```

### Launching Nginx
```bash
nginx -c $PWD/nginx.conf
```

## Usage
### Upload Source File to Server

Sample request:
```bash
curl -X POST -F source_file=@/tmp/myfile.mp3 http://127.0.0.1:8888/upload
```
Sample response:
```
{
    "source_id": "3e50836e-7b65-4fac-9e3e-81f7f5bb696b"
}
```

### Invoke ML Model
Sample request:
```bash
curl -i -H "Content-Type: application/json" -X POST \
  -d '{"source_id": "3e50836e-7b65-4fac-9e3e-81f7f5bb696b", "split_type": "spleeter:4stems"}' \
  http://127.0.0.1:8888/invoke
```
Sample response:
```
{
    "request_id":"2d85c022-bdee-4462-ab85-f9a12b6402d6"
}
```

### Check Request Status
Sample request:
```bash
curl -i http://127.0.0.1:8888/status/2d85c022-bdee-4462-ab85-f9a12b6402d6

```
Sample response:
```
{
    "output_artifacts":[
        "http://127.0.0.1:8888/artifacts/2d85c022-bdee-4462-ab85-f9a12b6402d6/myfile/accompaniment.wav",
        "http://127.0.0.1:8888/artifacts/2d85c022-bdee-4462-ab85-f9a12b6402d6/myfile/vocals.wav"
    ],
    "request_id":"2d85c022-bdee-4462-ab85-f9a12b6402d6",
    "status":"success"
}
```

### Download Results
```bash
wget http://127.0.0.1:8888/artifacts/2d85c022-bdee-4462-ab85-f9a12b6402d6/myfile/accompaniment.wav
```
