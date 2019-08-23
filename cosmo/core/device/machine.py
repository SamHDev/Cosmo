import subprocess


def shutdown():
    subprocess.call("shutdown -h now")


def restart():
    subprocess.call("shutdown -r -h now")
