# SoundPicker 
## About
**SoundPicker** is designed to work with audio files and use already trained state of the art models for performing separations and variouse sound extractions. The current version tests Spleeter a source separation library with pretrained models written in Python and uses Tensorflow. This implementation includes Vocals / accompaniment separation API usage. 


## Usage

% curl -i -H "Content-Type: application/json" -X POST -d '{"original_file": "/Users/user/Downloads/audiofile.mp3"}' http://127.0.0.1:8080/invoke



HTTP/1.0 200 OK

Content-Type: application/json

Content-Length: 239

Server: Werkzeug/2.0.1 Python/3.8.18

Date: Thu, 25 Jan 2024 05:35:26 GMT



{

  "output_files": [

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/accompaniment.wav", 

    "/var/folders/27/qyx8gdrd3sq4420y2snx24k88yzvn1/T/audiofile/vocals.wav"

  ], 

  "status": "success"

}