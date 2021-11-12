import subprocess
import os
import urllib
import zipfile
import time

DEVELOPER_DISK_IMAGE_URL = 'https://github.com/haikieu/xcode-developer-disk-image-all-platforms/raw/master/DiskImages/iPhoneOS.platform/DeviceSupport/{v}.zip'


def get_disk_image(version):
    print('Beginning file download...')
    download_loc = os.getcwd() + '\\' + version + '.zip'
    try:
        urllib.request.urlretrieve(
            DEVELOPER_DISK_IMAGE_URL.format(v=version), download_loc)
        print('Unzipping...')
        zipfile.ZipFile(download_loc).extractall()
        os.remove(download_loc)
    except urllib.error.HTTPError as e:
        print('Could not find Developer Disk Image (iOS ' + version + ').')
        time.sleep(5)


def mount_image(version):
    if not os.path.exists(os.getcwd() + '\\' + version):
        get_disk_image(version)
    cmd = 'cd ' + os.getcwd() + '\\ & ideviceimagemounter ' + os.getcwd() + '\\' + version + \
        '\\DeveloperDiskImage.dmg ' + os.getcwd() + '\\' + version + \
        '\\DeveloperDiskImage.dmg.signature'
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print('Developer Disk Image mounted!')
        return True
    except Exception as e:
        if 'Device is locked' in e.output.decode() or 'Could not start' in e.output.decode():
            print('Please unlock your device and try again.')
            time.sleep(5)
        return False


def set_location(coordinates):
    try:
        cmd = 'cd ' + os.getcwd() + '\\ & idevicesetlocation -- ' + coordinates
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print('Device location set to ' + coordinates + '.')
    except Exception as e:
        if 'Device is locked' in e.output.decode():
            print('Please unlock your device and try again.')
            time.sleep(5)
        elif 'No device found' in e.output.decode():
            print('Please connect your device.')
            time.sleep(5)
        elif 'Make sure a developer disk image is mounted!' in e.output.decode():
            cmd = 'cd ' + os.getcwd() + '\\ & ideviceinfo'
            version = [i for i in subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode(
            ).split('\n') if i.startswith('ProductVersion')][0].split(' ')[1][:4]
            if mount_image(version):
                set_location(coordinates)


def set_zju_location(long: float, lati: float):
    set_location(f"{lati + 0.002293} {long - 0.004769}")


def run_from_a_to_b(a_long: float, a_lati: float, b_long: float, b_lati: float, sec: int):
    d_long = (b_long - a_long) / sec
    d_lati = (b_lati - a_lati) / sec

    for i in range(sec + 1):
        set_zju_location(a_long + i * d_long, a_lati + i * d_lati)
        time.sleep(1)


# 120.124244,30.264259 左上
# 120.123836,30.263059 左下
# 120.124652,30.262823 右下
# 120.125086,30.264009 右上

while (True):
    run_from_a_to_b(120.124244, 30.264259, 120.123836, 30.263059, 24)
    run_from_a_to_b(120.123836, 30.263059, 120.124652, 30.262823, 14)
    run_from_a_to_b(120.124652, 30.262823, 120.125086, 30.264009, 24)
    run_from_a_to_b(120.125086, 30.264009, 120.124244, 30.264259, 14)
