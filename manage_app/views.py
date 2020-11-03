import logging
# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Models
from config_app.models import ConfigParameters, SNMPConfigParameters
from manage_app.models import DeviceModel, DeviceInterface, DeviceTrapModel, VarBindModel

# Backend
from visualize_app.backend.NetworkMapper import NetworkMapper
from .backend.DeviceManager import DeviceManager
from .backend.parse_model import parse_and_save_to_database, parse_trap_model
from .backend.webssh import main
from WebAppLAN_MonitorDjango.utils import get_available_devices

# Celery tasks
from .backend import tasks

ssh_session = None
task = None


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    global ssh_session, task

    device_trap_models = None
    device_details_output = None
    device_interfaces_output = None
    error_status_message = None

    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = ConfigParameters.objects.filter(snmp_config_id__isnull=False)[0].snmp_config_id

    SNMP_config = SNMPConfigParameters.objects.filter(id=snmp_config_id)[0]
    traps_enabled = SNMP_config.enable_traps
    traps_engine_running = SNMP_config.traps_activated

    request_post_dict = dict(request.POST)

    if 'get_devices_details' in request.POST:
        DeviceModel.objects.all().delete()
        DeviceInterface.objects.all().delete()

        available_hosts = get_available_devices()
        device = DeviceManager(user, available_hosts, snmp_config_id)
        devices_details_output = device.get_multiple_device_details()

        my_map = NetworkMapper()
        my_map.clear_graph_data()

        try:
            parse_and_save_to_database(devices_details_output, user)
        except Exception as exception:
            logging.basicConfig(format='!!! %(asctime)s %(message)s')
            logging.warning(exception)
            error_status_message = 'System was not able to get all SNMP data - check connection...'
    #
    # SNMP_config.traps_activated = False
    # SNMP_config.save()

    if 'start_trap_engine' in request.POST:
        if traps_enabled and not traps_engine_running:
            #task = tasks.run_trap_engine.delay()
            task = tasks.run_trap_enginev2.delay()

            SNMP_config.traps_activated = True
            SNMP_config.save()

    elif 'stop_trap_engine' in request.POST:
        if traps_enabled and traps_engine_running:
            task.revoke(terminate=True, signal='SIGUSR1')

            SNMP_config.traps_activated = False
            SNMP_config.save()

    elif 'get_device_details' in request.POST:
        device_id = request_post_dict.get('get_device_details')[0]

        device_details_output = DeviceModel.objects.filter(id=device_id)[0]
        device_interfaces_output = DeviceInterface.objects.filter(device_model_id=device_id)

        device_trap_models = DeviceTrapModel.objects.filter(device_model=device_details_output)

        trap_data = VarBindModel.objects.all()

        parse_trap_model(device_trap_models, trap_data)


    # TO DO!!!
    # elif 'run_ssh_session' in request.POST:
    #     ssh_session = main.main()
    #     ssh_session.start()
    #     # TO DO - aktualnie przy pomocy asyncio z głównego procesu django "forkuje" się subproces ktory stawia
    #     # clienta ssh, niestety glowny watek caly czas sie kreci - trzeba przekminic jak zforkowac clienta ssha zeby
    #     # to ładnie zagrało a potem zastanowic sie jak wpakowac tego klienta do mannage_app - do zrobienia

    print()
    context = {
        'ssh_session': ssh_session,
        'device_detail_output': device_details_output,
        'device_interfaces_output': device_interfaces_output,
        'devices_details_output': DeviceModel.objects.all(),
        'devices_interfaces_output': DeviceInterface.objects.all(),
        'error_status_message': error_status_message,
        'traps_engine_running': traps_engine_running,
        'traps_enabled': traps_enabled,
        'device_trap_models': device_trap_models,
    }

    return render(request, 'manage_network.html', context)
