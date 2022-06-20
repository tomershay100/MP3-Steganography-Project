# MP3 Steganography Web

MP3 Steganography Web is a one-page webApp that allows the user to have a convenient experience using the MP3Stego library. The frontend is built using `bootstrap` and communicates with a small `flask` server that runs the library functions by uploading the files and downloading the products.

## Features

### Converting ``MP3`` into ``WAV`` files (decode)
As you can see, in the `MP3 to WAV` tab you can upload ``MP3`` file and decode it into ``WAV`` file.
![alt text](https://github.com/tomershay100/MP3-Steganography-Project/blob/main/mp3%20steganography%20web/images/decode.png?raw=true)

### Converting ``WAV`` into ``MP3`` files (encode)
You can also upload ``WAV`` file and encode it into ``MP3`` file by uploading the file and specify the ``bitrate`` of the ``WAV`` file at the `WAV to MP3 tab`.
![alt text](https://github.com/tomershay100/MP3-Steganography-Project/blob/main/mp3%20steganography%20web/images/encode.png?raw=true)

### Hiding String in MP3 file
The main function of our library is the hiding function. By uploading ``MP3`` file and ``TXT`` file, the output of the function is a ``MP3`` file with the text hidden in it . A further explanation of the hiding process can be found in the related article.
![alt text](https://github.com/tomershay100/MP3-Steganography-Project/blob/main/mp3%20steganography%20web/images/hide.png?raw=true)

### Reveal String from MP3 file
Another function of our library is the revealing function. You can upload ``MP3`` file and out library will find the hidden string in it, and download the resulting ``TXT`` file.
![alt text](https://github.com/tomershay100/MP3-Steganography-Project/blob/main/mp3%20steganography%20web/images/reveal.png?raw=true)

### Clearing String from MP3 file
The last tab allows the user to upload ``MP3`` file and get new clear ``MP3`` file that contains the same audio.  
![alt text](https://github.com/tomershay100/MP3-Steganography-Project/blob/main/mp3%20steganography%20web/images/clear.png?raw=true)

## Dependencies

1. [Python 3](https://www.python.org/downloads/)
2. [flask](https://flask.palletsprojects.com/en/2.1.x/installation/)
3. [mp3stego](https://pypi.org/project/mp3stego-lib/)
4. [werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/installation/)

## Running Instructions
```shell 
    python3 app.py
```
