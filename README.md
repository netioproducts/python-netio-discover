# Python Netio Discover Class

Automatically detect all interfaces and sends UDP discover to search new NETIO devices on connected interfaces.



##Requirements
- Linux
- pypi netifaces
- Python 2.7

tested for IPv4 and Ubuntu 18.04

##Usage:
- NetioDiscover.py - the main class with discover
- discover.py - example script

run `sudo python discover.py`

Interfaces can be specified in list of interface names in object constructor. `discovery = NetioDiscover(["enp0s25", "wlp2s0"])`
 
By default it scans all found interfaces. `discovery = NetioDiscover()`

has to be run with sudo privileges due to work with broadcast on network interfaces

