"""Commands related to networks are in this module"""
import click
import sys
from hil.cli.client_setup import client
from prettytable import PrettyTable
import json

@click.group()
def network():
    """Commands related to network"""


@network.command(name='create', short_help='Create a new network')
@click.argument('network')
@click.argument('owner')
@click.option('--access', help='Projects that can access this network. '
              'Defaults to the owner of the network')
@click.option('--net-id',
              help='Network ID for network. Only admins can specify this.')
def network_create(network, owner, access, net_id):
    """Create a link-layer <network>.  See docs/networks.md for details"""
    if net_id is None:
        net_id = ''
    if access is None:
        access = owner
    client.network.create(network, owner, access, net_id)


@network.command(name='delete')
@click.argument('network')
def network_delete(network):
    """Delete a network"""
    client.network.delete(network)


@network.command(name='show')
@click.argument('network')
def network_show(network):
    """Display information about network"""
    q = client.network.show(network)
    x = PrettyTable()
    x.field_names = ['attribute', 'info']
    for item, value in q.iteritems():
        if item != 'connected-nodes':
            if isinstance(value, unicode):
                x.add_row([item,value])
            else:
                x.add_row([item,value[0].encode("utf-8")])
        else:
            for key1,value1 in value.iteritems():
                x.add_row([item.encode("utf-8"),key1.encode("utf-8")])
    print(x)


@network.command(name='list')
def network_list():
    """List all networks"""
    q = client.network.list()
    count=0
    x = PrettyTable()
    x.field_names = ['network name','network id','project name']
    for key1,value1 in q.iteritems():
        for key2,value2 in value1.iteritems():
            if count%2==0:
                pid=value2
            else:
                pname=value2
            count+=1
        x.add_row([key1,pid,pname[0].encode("utf-8")])
    print(x)     
    



@network.command('list-attachments')
@click.argument('network')
@click.option('--project', help='Name of project.')
def list_network_attachments(network, project):
    """Lists all the attachments from <project> for <network>

    If <project> is `None`, lists all attachments for <network>
    """
    print client.network.list_network_attachments(network, project)


@network.command(name='grant-access')
@click.argument('network')
@click.argument('project')
def network_grant_project_access(project, network):
    """Add <project> to <network> access"""
    client.network.grant_access(project, network)


@network.command(name='revoke-access')
@click.argument('network')
@click.argument('project')
def network_revoke_project_access(project, network):
    """Remove <project> from <network> access"""
    client.network.revoke_access(project, network)
