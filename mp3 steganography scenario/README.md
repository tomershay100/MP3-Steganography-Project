# MP3-Steganography-Scenario
This repository presents an example scenario where our system (or any MP3 steganography system) could be put to use:

Say our agent, Alice (`client.py`), has an open shell command line where she wants to run some commands or scripts. This
shell is open on a remote server (`server.py`) and is remotely controlled, thus Alice must send commands remotely over a
network. However, Alice does not want to send those commands openly over the network, as the channel she uses to
communicate with the remote server is insecure. This can be caused by two reasons: 
A) Alice is an attacker in an “enemy” network. She has managed to control her own region in a server of that network (namely, the remotely controlled shell on
the server), but does not want the ones controlling the network to see her commands sent to the shell, or even suspect
that Alice’s traffic are malicious commands.

B) Alice actually controls the server in which the shell runs, but she suspects of man-in-the-middle attackers sniffing traffic on the channel. She does not want such a potential attacker to
sniff out her commands (she could use cryptography to hide the content she sends over the channel, but she does not want
the attacker to even suspect she sends those commands). 

To protect her commands and hide their existence on the insecure
channel, Alice turns to steganography. On her end, Alice downloads a MP3 file of an unsuspicious nature - say, a MP3
version of the hit song “Never Gonna Give You Up” by Rick Astley. She then uses the custom MP3 steganography system to
decode the file and re-encode it, embedding her secret message within - in her case, a shell script she wishes to run in
the server. She then sends the MP3 stego-file through the insecure channel to the server. Any attacker sniffing the
traffic over the channel will only see a MP3 file of “Never Gonna Give You Up” transferring to the server. This is
probably less suspicious traffic than shell commands in plain text, or even weird encrypted messages - unless the
attacker specifically knows Alice uses steganography, they will probably have no idea about the script hidden in the MP3
file. When the file arrives at the server, Alice is in the clear. She can use the custom MP3 decoder to retrieve the
script she hid inside the file, and with some code, have her shell run it. As only the channel itself is insecure, any
sniffer will never even know Alice was the one who ran these scripts!
