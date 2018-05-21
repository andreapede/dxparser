import telnetlib  # for telnet communication
import re
import time

server_ip = "dxcluster.iz0tws.com"  # dxcluster.iz0tws.com"
server_port = 7300  # port number of the cluster
user = "iz0twd"  # callsign to register in the cluster
password = ""  # if needed

# Open connection to telnet
tn = telnetlib.Telnet(host=server_ip, port=server_port)

tn.read_until(b"login: ")

tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

# Define regular expressions +b"\s+(.*)"
callsign_pattern = b"([a-z|0-9|/]+)"
frequency_pattern = b"([0-9|.]+)"
pattern = re.compile(
    b"^DX de " + callsign_pattern + b":\s+" + frequency_pattern + b"\s+" + callsign_pattern + b"\s+(.*)\s+(\d{4}Z)",
    re.IGNORECASE)
# Parse telnet
while (1):
    # Check new telnet info against regular expression
    telnet_output = tn.read_until(b"\r\n", timeout=10)
    print(time.localtime());
    print(telnet_output)
    match = pattern.match(telnet_output)
    print(match)
    # If there is a match, sort matches into variables
    if match:
        spotter = match.group(1)
        frequency = float(match.group(2))
        spotted = match.group(3)
        comment = match.group(4).strip()
        spot_time = match.group(5)
        # band = frequency_to_band(frequency)
        print(spotter, frequency, spotted, comment, spot_time)
