from NetioDiscover import NetioDiscover

discovery = NetioDiscover(["enp0s25", "wlp2s0"])

print(discovery.getDevicesLinux())

