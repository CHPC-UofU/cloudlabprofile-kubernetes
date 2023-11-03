"""A test profile with N Rocky Linux 9 nodes designed to test Kubernetes installation and configuration automation.

Instructions:
Wait for the profile instance to start. Then begin work.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as igext

# Define OS image
OS_IMAGE = 'urn:publicid:IDN+emulab.net+image+emulab-ops:ROCKY9-64-STD'

# Create a portal context, needed to define parameters
context = portal.Context()

# Create a Request object to start building RSpec
request = context.makeRequestRSpec()

# Create some user-configurable parameters
context.defineParameter('node_count',
                        'The number of nodes to allocate',
                        portal.ParameterType.INTEGER,
                        2)
context.defineParameter('public_ip_count',
                        'The number of additional public IPs to allocate',
                        portal.ParameterType.INTEGER,
                        2)

params = context.bindParameters()

# Validate parameters:
if params.node_count < 2:
    context.reportError(
        portal.ParameterError('You must allocate at least 1 additional node.',
                                              ['node_count']))
if params.public_ip_count < 2:
    context.reportError(
        portal.ParameterError('You must allocate at least 1 additional public ip.',
                              ['public_ip_count']))
context.verifyParameters()

# Create a LAN:
if params.node_count == 2:
    lan = request.Link()
else:
    lan = request.LAN()

# Set up the nodes:
ipv4_last_octet = 1
for i in range(params.node_count):
    ipv4_addr = "10.10.1." + str(ipv4_last_octet)
    ipv4_last_octet += 1

    node = request.XenVM("vm%02d" % i)
    node.disk_image = OS_IMAGE

    iface = node.addInterface("eth1")
    iface.addAddress(pg.IPv4Address(ipv4_addr, "255.255.255.0"))

    lan.addInterface(iface)
    request.addResource(node)

# Add LAN to request:
request.addResource(lan)

# Request a pool of dynamic publicly routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('MetalLBPool', int(params.public_ip_count))
request.addResource(addressPool)

# Output RSpec
context.printRequestRSpec(request)
