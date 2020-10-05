from config_app.models import ConfigParameters, SNMPConfigParameters
from config_app.backend.static import device_os


def parse_initial_config(object_id):
    config = {
        "user": {
            "username": None,
            "password": None,
            "secret": None,
        },
        "ip_range": {
            "network_ip": None,
            "subnet": None
        },
        "system": {
            "network_dev_os": None,
            "discovery_proto": None

        }
    }

    config_obj = ConfigParameters.objects.filter(id=object_id)[0]

    config["user"]["username"] = config_obj.login_username
    config["user"]["password"] = config_obj.login_password
    config["user"]["secret"] = config_obj.secret

    config["ip_range"]["network_ip"] = config_obj.network_ip
    config["ip_range"]["subnet"] = config_obj.subnet_cidr

    config["system"]["network_dev_os"] = device_os.get(config_obj.network_device_os, 'cisco_ios')
    config["system"]["discovery_proto"] = config_obj.discovery_protocol

    login_params_napalm = {'username': config['user'].get('username'), 'password': config['user'].get('password'),
                           'optional_args': {'secret': config['user'].get('secret')}}

    login_params_netmiko = {'username': config['user'].get('username'), 'password': config['user'].get('password'),
                            'secret': config['user'].get('secret'),
                            'device_type': config['system'].get('network_dev_os')

                            }

    login_params = {'netmiko': login_params_netmiko, 'napalm': login_params_napalm}

    return config, login_params


def parse_snmp_config(object_id):
    configure_commands = list()
    snmp_config = SNMPConfigParameters.objects.filter(id=object_id)[0]
    basic_command = "snmp-server"

    configure_commands.append("{basic_command} enable".format(basic_command=basic_command))

    if snmp_config.enable_traps:
        configure_commands.append("{basic_command} enable traps".format(basic_command=basic_command))
    if snmp_config.server_location:
        configure_commands.append("{basic_command} location {loaction}".format(basic_command=basic_command,
                                                                               loaction=snmp_config.server_location))
    if snmp_config.contact_details:
        configure_commands.append("{basic_command} contact {contact}".format(basic_command=basic_command,
                                                                             contact=snmp_config.contact_details))

    configure_commands.append(
        "{basic_command} group {group} v3 priv".format(basic_command=basic_command, group=snmp_config.group_name))

    configure_commands.append(
        "{basic_command} user {user} {group} v3 auth md5 {password} priv aes 128 {encrypt_key}".format(
            basic_command=basic_command, user=snmp_config.snmp_user, group=snmp_config.group_name,
            password=snmp_config.snmp_password, encrypt_key=snmp_config.snmp_encrypt_key))

    configure_commands.append("{basic_command} host {host} version 3 {user}".format(basic_command=basic_command,
                                                                                    host=snmp_config.snmp_host,
                                                                                    user=snmp_config.snmp_user))

    return configure_commands


def remove_snmp_config(commands):
    return ["no {command}".format(command=command) for command in commands]
