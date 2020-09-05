import os

import click
from click import style, echo

from configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel

CMD_SEP = style('-----', fg='cyan')


@click.command('chainlink:create')
@click.argument('path', default=os.getcwd())
def chainlink_create(path):
    echo(style('Welcome to Chainchomp. We can see that you want to add a new chainlink', fg='cyan'))
    echo(style('What is the project that this chainlink is assigned to', fg='cyan'))
    # TODO list currently available projects and offer choice before new project needs to be created
    project_name = click.prompt('Please type in the designated project name now')
    echo(style('Now please provide a name for your chainlink', fg='cyan'))
    chainlink_name = click.prompt('Please type in the designated name now')
    chainlink_config_model = ChainlinkConfigModel(project_name, chainlink_name)

    more_information = click.confirm(style('Do you want to input further details?', fg='cyan'), default=False)
    if not more_information:
        return
    master_link = click.confirm('Is this chainlink a Master link?', default=chainlink_config_model.is_master_link)
    if not master_link:
        master_location = click.prompt('Do you want to provide information about the master link location?',
                                       default=False)
        if master_location:
            master_location = click.prompt('Please provide an ip address for the master chainlink',
                                           default=chainlink_config_model.master_location)
            chainlink_config_model.master_location = master_location

    start_script = click.confirm(style('Do you want to provide information about a start script', fg='cyan'),
                                 default=False)
    if start_script:
        start_command = click.prompt('Please provide a full command to execute your start script now',
                                     default=chainlink_config_model.start)
        chainlink_config_model.start = start_command

    stop_script = click.confirm(style('Do you want to provide information about a stop script', fg='cyan'),
                                default=False)
    if stop_script:
        stop_command = click.prompt('Please provide a full command to execute your stop script now',
                                    default=chainlink_config_model.stop)
        chainlink_config_model.stop = stop_command

    mq = click.confirm(style('Do you want to provide information about the message queue type', fg='cyan'),
                       default=False)
    if mq:
        default = 1 if chainlink_config_model.mq_type == 'rabbitmq' else 2
        mq_type = click.prompt('Please choose one of the following by number \n'
                               '1) RabbitMQ\n'
                               '2) Apache Kafka\n',
                               default=default)
        chainlink_config_model.mq_type = mq_type


@click.command('chainlink:edit')
def chainlink_edit():
    pass


@click.command('chainlink:start')
def chainlink_start():
    pass


@click.command('chainlink:stop')
def chainlink_stop():
    pass


@click.command('chainlink:ping')
def chainlink_ping():
    pass


@click.command('chainlink:mq')
def chainlink_mq():
    pass


@click.command('chainchomp:profile')
def chainchomp_profile():
    pass


@click.command('chainchomp:project')
def chainchomp_project():
    pass
