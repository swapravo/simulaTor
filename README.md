# simulaTor

A simulation of the The Onion Router


# Demo

In order to start the network, use

    sudo ./run

This will start:
    2 X TOR Directory Nodes,
    2 X Gaurd Relays
    2 X Middle Relays
    2 X Exit Relays

In order to bring the server and the client up, use

<br>

    ./server/server.py
    ./clients/client.py


<br><br>
<br>

## Steps

<br>
Here is how it works:
<br>
<br><br>
Step 1:
Each Node upon starting up, generates Asymmetric keys for itself and reports their presence and its to the directory Node.
<br>
<br>
Step 2:
When the client comes online, it requests the directory node for all available relays.
Chooses 1 Gaurd, 1 Middle & 1 Exit relay for itself and requests them for a bootstrap.
<br>
<br>
Step 3:
Upon receiving a request to Bootstrap from the client, each selected node recursively sends a boostraping request to the next node. These nodes find each other and compute a shared symmetric Key.
<br>
<br>
Step 4:
Such requests are communicate using GET/POST requests.
Each request is encrypted using ECDH before being encoded with base64.
<br>
<br>
Upon completion of the bootstrapping process, the client sends a message to the server.
<br>
<br>
This message is first encrypted using the symmetric key shared by the client and the exit relay and then by the symmetric key shared by the client and the middle relay and then by the symmetric key shared by the client and the gaurd relay.
<br>
<br>
This message is then relayed from each relays' "virtual router" to the next one, until it reaches the server.
<br>
<br>
Responses from the server are encrypted by each of the nodes. Upon reaching the client, they are decrypted.

