#!/usr/bin/env python

"""This CloudLab profile allocates N Rocky9 XenVM nodes, allocates routable IPv4s for each, adds an address pool of N IPv4s (for MetalLB), and connects them directly together via a LAN.

Instructions:
Click on any node in the topology and choose the `shell` menu item. When your shell window appears, use `ping` to test the link.
"""

import geni.portal as portal
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
                        3)
context.defineParameter('public_ip_count',
                        'The number of additional public IPs to allocate',
                        portal.ParameterType.INTEGER,
                        2)

params = context.bindParameters()

# Validate parameters:
if params.node_count < 3:
    context.reportError(
        portal.ParameterError('You must allocate at least three nodes.',
                                              ['node_count']))
if params.public_ip_count < 2:
    context.reportError(
        portal.ParameterError('You must allocate at least 1 additional public ip.',
                              ['public_ip_count']))
context.verifyParameters()

# Create the best effort LAN between the VM nodes.
lan = request.LAN()
lan.best_effort = True

# Add VMs to the request that can be accessed from the public Internet.
for i in range(params.nodeCount):
    vmName = "%s-%d" % ('vm', i)
    node = request.XenVM(vmName)
    node.cores = 4
    node.ram = 8192
    node.routable_control_ip = True
    node.disk_image = params.osImage
    iface = node.addInterface("eth1")
    lan.addInterface(iface)

# Request a pool of dynamic publicly routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('MetalLBPool', int(params.public_ip_count))
request.addResource(addressPool)

# Print the RSpec to the enclosing page.
context.printRequestRSpec(request)
