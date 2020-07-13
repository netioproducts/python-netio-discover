from NetioDiscover import NetioDiscover
import pprint
discovery = NetioDiscover()
pp = pprint.PrettyPrinter(indent=2)

pp.pprint(discovery.getDevicesLinux())

