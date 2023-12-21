import datetime

import psutil
import uuid

class MachineState:
    def __init__(self):

        self.UUID = str(uuid.UUID(int=uuid.getnode()))
        cpufreq = psutil.cpu_freq()
        self.physicalСores = f"{psutil.cpu_count(logical=False)}"
        self.totalCores = f"{psutil.cpu_count(logical=True)}"
        self.frequencyMax = f"{cpufreq.max:.2f}MHz"
        self.frequencyMin = f"{cpufreq.min:.2f}MHz"
        self.frequencyСurrent = f"{cpufreq.current:.2f}MHz"
        self.cpuPercent = f"{psutil.cpu_percent()}%"
        self.cpuPercentForCore = getPercentForCore()
        svmem = psutil.virtual_memory()
        self.totalSizeMemory = f"{getSize(svmem.total)}"
        self.availableSizeMemory = f"{getSize(svmem.available)}"
        self.usedSizeMemory = f"{getSize(svmem.used)}"
        self.percentMemory = f"{svmem.percent}%"
        swap = psutil.swap_memory()
        self.totalSizeSwapMemory = f"{getSize(swap.total)}"
        self.freeSizeSwapMemory = f"{getSize(swap.free)}"
        self.usedSizeSwapMemory = f"{getSize(swap.used)}"
        self.percentSwapMemory = f"{swap.percent}%"
        self.diskInfo = getDiskInfo()
        self.webInfo = getWebInfo()
        net_io = psutil.net_io_counters()
        self.webByteSent = f"{getSize(net_io.bytes_sent)}"
        self.webByteRecv = f"{getSize(net_io.bytes_recv)}"
        # температура только для linux
        self.temp = getTemp()
        self.timeCreateMSK = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))))


def getSize(bytes, suffix="B"):
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def getTemp():
    string = ""
    if not hasattr(psutil, "sensors_temperatures"):
        return ("платформа не поддерживается")
    temps = psutil.sensors_temperatures()
    if not temps:
        return ("не могу определить никакую температуру")
    for name, entries in temps.items():
        for entry in entries:
            string += ("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
                entry.label or name, entry.current, entry.high,
                entry.critical))
    return string


def getPercentForCore():
    str = ""
    for i, perecentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        str += f"Core{i}:{perecentage}%;"

    return str


def getDiskInfo():
    partitions = psutil.disk_partitions()
    str = ""
    for partition in partitions:
        str += f"Disk: {partition.device}; File System Type: {partition.fstype};"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:

            continue
        str += f" Общий обьем на дисках: {getSize(partition_usage.total)}; "
        str += f"Используется : {getSize(partition_usage.used)}; "
        str += f"Свободно : {getSize(partition_usage.free)}; "
        str += f"Процент : {partition_usage.percent}%; "

    return str


def getWebInfo():
    if_addrs = psutil.net_if_addrs()
    strin = ""
    for interface_name, interface_adresses in if_addrs.items():
        for address in interface_adresses:
            strin += f"Interface: {interface_name}"
            if str(address.family) == 'AddressFamily.AF_INET':
                strin += f"IP: {address.address}; "
                strin += f"Сетевая маска: {address.netmask}; "
                strin += f"Широковещательный IP-адрес : {address.broadcast}; "
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                strin += f"MAC-адрес: {address.address}; "
                strin += f"Сетевая маска: {address.netmask}; "
                strin += f"Широковещательный MAC-адрес: {address.address}; "
    return strin
