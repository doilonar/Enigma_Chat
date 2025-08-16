# Enigma_Chat


Enigma_Chat is a command-line chat application that enables two users to communicate securely over a network. All messages are encrypted using a Python-based simulation of the historical Enigma machine.

## How It Works

The application uses a client-server model built with Python's `socket` library. Before communication begins, both the client and the server must configure their Enigma machine simulation with the exact same settings. These settings function as the shared secret key for encryption and decryption.

The core of the project is the `Enigma` class, which simulates the electromechanical rotor machine. It includes:
*   **Three Rotors (`alpha`, `beta`, `gama`):** These rotors permute the characters. After each character is encrypted, the rotors turn, changing the encryption for the next character.
*   **A Plugboard (`steckerbrett`):** This allows for swapping pairs of letters before and after they pass through the rotors, adding another layer of encryption.
*   **A Reflector (`reflector`):** After passing through the rotors, the signal hits a reflector which sends it back through the rotors in a different path. This ensures that encrypting a letter `X` to `Y` also means encrypting `Y` results in `X`, simplifying the decryption process.

For communication to be successful, both users must enter the identical initial rotor positions and plugboard settings.

## Getting Started

### Prerequisites
- Python 3

### Usage
No installation is required. Simply download or clone `main.py` and run it from your terminal.

**Step 1: Start the Server**

The first user must act as the server.
1. Run the script:
   ```bash
   python main.py
   ```
2. When prompted, choose `s` for Server.
3. Enter the IP address you want to host on (e.g., `127.0.0.1` for local testing, or your machine's local network IP) and a port number (e.g., `9999`).
4. Enter the shared secret key: the initial integer positions for the `alpha`, `beta`, and `gama` rotors, and the three letter-pairs for the plugboard.

**Example Server Setup:**
```
$ python main.py
###############
# ENIGMA CHAT #
###############
Server/Client?(s/c): s
IP: 127.0.0.1
PORT: 9999
alpha: 5
beta: 12
gama: 20
0 in_character: q
0 out_character: w
1 in_character: e
1 out_character: r
2 in_character: t
2 out_character: y
Waiting...
```

**Step 2: Start the Client**

The second user acts as the client.
1. Run the script:
   ```bash
   python main.py
   ```
2. When prompted, choose `c` for Client.
3. Enter the server's IP address and port number.
4. **Crucially, enter the exact same Enigma settings (rotor positions and plugboard pairs) that the server used.**

**Example Client Setup:**
```
$ python main.py
###############
# ENIGMA CHAT #
###############
Server/Client?(s/c): c
IP: 127.0.0.1
PORT: 9999
alpha: 5
beta: 12
gama: 20
0 in_character: q
0 out_character: w
1 in_character: e
1 out_character: r
2 in_character: t
2 out_character: y
Connected with ('127.0.0.1', <port_number>)
```

**Step 3: Chat**

Once connected, users can type messages and press Enter. The application will display:
*   The raw encrypted message being sent/received.
*   The decrypted plain text message.

To end the session, either user can type `exit`.
