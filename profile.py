"""
A test profile with N Rocky Linux 9 nodes designed to test Kubernetes installation and configuration automation.

Instructions:
Wait for the profile instance to start. Then begin work.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as igext

# Define OS image
OS_IMAGE = 'urn:publicid:IDN+emulab.net+image+emulab-ops:ROCKY9-64-STD'

# Create a portal context, needed to define parameters
pc = portal.Context()

# Create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# Create some user-configurable parameters
pc.defineParameter('node_count',
                   'The number of nodes to allocate',
                   portal.ParameterType.INTEGER,
                   2)
pc.defineParameter('public_ip_count',
                   'The number of additional public IPs to allocate',
                   portal.ParameterType.INTEGER,
                   2)

params = pc.bindParameters()

# Validate parameters:
if params.node_count < 2:
    pc.reportError(portal.ParameterError('You must allocate at least 1 additional node.', ['node_count']))
if params.public_ip_count < 2:
    pc.reportError(portal.ParameterError('You must allocate at least 1 additional public ip.', ['public_ip_count']))
pc.verifyParameters()

# Create LAN with 1 GB/s bandwidth:
lan = pg.LAN()
lan.bandwidth = 1000000  # This is in kbps.

# Set up node names:
aliases = []
for i in range(params.node_count):
    aliases.append("node%02d" % i)

# Set up the nodes:
ipv4_last_octet = 1
for i in range(params.node_count):
    node = request.RawPC(aliases[i])
    node.disk_image = OS_IMAGE

    ipv4_addr = "10.10.1." + str(ipv4_last_octet)
    ipv4_last_octet += 1

    iface = node.addInterface("eth1")
    iface.addAddress(pg.IPv4Address(ipv4_addr, "255.255.255.0"))
    lan.addInterface(iface)

# Add LAN to request:
request.addResource(lan)

# Request a pool of dynamic publicly routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('addressPool', int(params.public_ip_count))
request.addResource(addressPool)

# Output RSpec
pc.printRequestRSpec(request)
