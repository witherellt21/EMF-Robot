
import struct
import time

# Try MicroPython

import smbus
from pyb import I2C

def _initBus(bus): 
    return I2C(bus, I2C.MASTER)

def _writeRegister(bus, address, subAddress, data): 
    bus.mem_write(data, address, subAddress)

def _readRegisters(bus, address, subAddress, count):
    return bus.mem_read(count, address, subAddress)

# Default to Raspberry Pi


def _initBus(bus): 
    return smbus.SMBus(bus)

def _writeRegister(bus, address, subAddress, data): 
    bus.write_byte_data(address, subAddress, data)

def _readRegisters(bus, address, subAddress, count):
    bus.write_byte(address, subAddress)
    return [bus.read_byte(address) for k in range(count)]
