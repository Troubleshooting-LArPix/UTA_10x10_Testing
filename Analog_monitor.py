import sys
import argparse
import json
import time

# larpix imports
import larpix
import larpix.io
import base

# defining defaults
_default_controller_config = None
parser = argparse.ArgumentParser()
parser.add_argument('--controller_config', default=_default_controller_config, type=str
    , help='''Hydra network configuration file''')
args = parser.parse_args()

# Creating controller from base.
c = base.main(**vars(args), logger=False)


print('\n----------------------------------------')
print('Human, You have started the analog monitor.')
print('----------------------------------------\n')

Condition = True
while Condition:
    print('\n')
    _chip_key = input("Enter the chip key:  ")
    _channel  = int(input("Enter a channel number:  "))

    print("Configuring the channel")
    # This allows the monitor to reset.
    try:
        c[_chip_key].config.enable_periodic_reset = 1
        c.write_configuration(_chip_key, 'enable_periodic_reset')
        # Foring the configuration to take.
        ok,diff = c.enforce_configuration(_chip_key,timeout=0.01,n=10,n_verify=10)
        if not ok:
            print('config error',diff)

        c.enable_analog_monitor(_chip_key, _channel)
        hold = input("Press ENTER when done")
        c.disable_analog_monitor(_chip_key, _channel)
    except ValueError:
        print('[ERROR] Invalid chip/channel combination!')

    Condition = input("Do you want to look at another? [y/n]")
    if Condition != 'y':
        Condition = False
        
