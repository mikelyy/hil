"""Commands related to node are in this module"""
import click
import sys
from hil.cli.client_setup import client
from prettytable import PrettyTable

@click.group()
def node():
    """Commands related to node"""


@node.command(name='list')
@click.argument('pool', type=click.Choice(['free', 'all']), required=True)
def nodes_list(pool):
    """List all nodes or free nodes"""
    q = client.node.list(pool)
    x=PrettyTable(['node list'])
    for node in q:
        x.add_row([node])
    print(x)


@node.command(name='show')
@click.argument('node')
def node_show(node):
    """Show node information"""
    q = client.node.show(node)
    x = PrettyTable()
    x.field_names = ['attribute','information']
    for item,value in q.iteritems():
        if isinstance(item, unicode):
            item = item.encode("utf-8") 
        if item == 'metadata':
            for key0,value0 in value.iteritems():
                temp1=[key0.encode("utf-8"),value0.encode("utf-8").strip('""')]
                x.add_row([item,":".join(temp1)])   
        elif item == 'nics':
            for key1,value1 in value[0].iteritems():
                if key1=='networks':
                    for key2,value2 in value1.iteritems():
                        #temp2=[key1.encode("utf-8"),":".join([key2.encode("utf-8"),value2.encode("utf-8")])]
                        #x.add_row([item,":".join(temp2)])
                        
                        x.add_row([key1.encode("utf-8"),":".join([key2.encode("utf-8"),value2.encode("utf-8")])])
                else:
                    #x.add_row([item,":".join([key1.encode("utf-8"),value1.encode("utf-8")])])
                    x.add_row([key1.encode("utf-8"),value1.encode("utf-8")])
        else:
            x.add_row([item,value])
    print(x)

                
    
    


@node.command(name='bootdev', short_help="Set a node's boot device")
@click.argument('node')
@click.argument('bootdev')
def node_bootdev(node, bootdev):
    """
    Sets <node> to boot from <dev> persistently

    eg; hil node_set_bootdev dell-23 pxe
    for IPMI, dev can be set to disk, pxe, or none
    """
    client.node.set_bootdev(node, bootdev)


@node.command(name='register', short_help='Register a new node')
@click.argument('node')
@click.argument('obmd-uri')
@click.argument('obmd-admin-token')
@click.argument('obmtype')
@click.argument('hostname')
@click.argument('username')
@click.argument('password')
def node_register(node,
                  obmd_uri,
                  obmd_admin_token,
                  obmtype,
                  hostname,
                  username,
                  password):
    """Register a node named <node>, with the given type
        if obm is of type: ipmi then provide arguments
        "ipmi", <hostname>, <ipmi-username>, <ipmi-password>
    """
    client.node.register(
        node,
        obmd_uri,
        obmd_admin_token,
        obmtype,
        hostname,
        username,
        password)


@node.command(name='delete')
@click.argument('node')
def node_delete(node):
    """Delete a node"""
    client.node.delete(node)


@node.group(name='network')
def node_network():
    """Perform node network operations"""


@node_network.command(name='connect', short_help="Connect a node to a network")
@click.argument('node')
@click.argument('nic')
@click.argument('network')
@click.argument('channel', default='', required=False)
def node_network_connect(node, network, nic, channel):
    """Connect <node> to <network> on given <nic> and <channel>"""
    print client.node.connect_network(node, nic, network, channel)


@node_network.command(name='detach', short_help="Detach node from a network")
@click.argument('node')
@click.argument('nic')
@click.argument('network')
def node_network_detach(node, network, nic):
    """Detach <node> from the given <network> on the given <nic>"""
    print client.node.detach_network(node, nic, network)


@node.group(name='nic')
def node_nic():
    """Node's nics commands"""


@node_nic.command(name='register')
@click.argument('node')
@click.argument('nic')
@click.argument('macaddress')
def node_nic_register(node, nic, macaddress):
    """
    Register existence of a <nic> with the given <macaddr> on the given <node>
    """
    client.node.add_nic(node, nic, macaddress)


@node_nic.command(name='delete')
@click.argument('node')
@click.argument('nic')
def node_nic_delete(node, nic):
    """Delete a <nic> on a <node>"""
    client.node.remove_nic(node, nic)


@node.group(name='obm')
def obm():
    """Commands related to obm configuration"""


@obm.command()
@click.argument('node')
def enable(node):
    """Enable <node>'s obm"""
    client.node.enable_obm(node)


@obm.command()
@click.argument('node')
def disable(node):
    """Disable <node>'s obm"""
    client.node.disable_obm(node)


@node.group(name='power')
def node_power():
    """Perform node power operations"""


@node_power.command(name='off')
@click.argument('node')
def node_power_off(node):
    """Power off <node>"""
    client.node.power_off(node)


@node_power.command(name='on')
@click.argument('node')
def node_power_on(node):
    """Power on <node>"""
    client.node.power_on(node)


@node_power.command(name='cycle')
@click.argument('node')
def node_power_cycle(node):
    """Power cycle <node>"""
    client.node.power_cycle(node)


@node.group(name='metadata')
def node_metadata():
    """Node metadata commands"""


@node_metadata.command(name='add', short_help='Add metadata to node')
@click.argument('node')
@click.argument('label')
@click.argument('value')
def node_metadata_add(node, label, value):
    """Register metadata with <label> and <value> with <node> """
    client.node.metadata_set(node, label, value)


@node_metadata.command(name='delete', short_help='Delete node metadata')
@click.argument('node')
@click.argument('label')
def node_metadata_delete(node, label):
    """Delete metadata with <label> from a <node>"""
    client.node.metadata_delete(node, label)


@node.group(name='console')
def node_console():
    """Console related commands"""


@node_console.command(name='show', short_help='Show console')
@click.argument('node')
def node_show_console(node):
    """Display console log for <node>"""
    print(client.node.show_console(node))


@node_console.command(name='start', short_help='Start console')
@click.argument('node')
def node_start_console(node):
    """Start logging console output from <node>"""
    client.node.start_console(node)


@node_console.command(name='stop', short_help='Stop console')
@click.argument('node')
def node_stop_console(node):
    """Stop logging console output from <node> and delete the log"""
    client.node.stop_console(node)
