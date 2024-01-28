# SoundPicker 
## About
**SoundPicker** is designed to work with audio files and use already trained state of the art models for performing separations and variouse sound extractions. The current version tests Spleeter a source separation library with pretrained models written in Python and uses Tensorflow. This implementation includes Vocals / accompaniment separation API usage. 


## Usage
```
% % curl -i -H "Content-Type: application/json" -X POST -d '{"original_file": "/Users/user/Downloads/audiofile.mp3", "split_type": "spleeter:4stems"}' http://127.0.0.1:8080/invoke
```

```
HTTP/1.0 200 OK

Content-Type: application/json

Content-Length: 508

Server: gunicorn

Date: Sun, 28 Jan 2024 08:27:40 GMT

```

```
{

  "output_files": [

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/accompaniment.wav", 

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/drums.wav", 

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/vocals.wav", 

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/other.wav", 

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/bass.wav"

  ], 

  "status": "success"

} 

```
