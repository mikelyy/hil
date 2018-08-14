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
    for item in q.items():
        x.add_column(x.field_names[0],['access','channels','owner','name','connected-nodes'])
        x.add_column(x.field_names[1],item[1][0],item[1][1],item[1][2],item[1][3],item[1][4])
    print(x)


@network.command(name='list')
def network_list():
    """List all networks"""
    q = client.network.list()
    x = PrettyTable()
    for item in q.items():
        x.add_row([item[0],item[1]])
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
