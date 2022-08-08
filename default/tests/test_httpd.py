import http
import unittest
import os
import pytest
from subprocess_tee import run
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# def test_hosts_file(host):
#     f = host.file('/etc/hosts')

#     # EXAMPLE_7 break TestInfra by testing that /etc/hosts does not esist
#     assert f.exists is True
#     assert f.user == 'root'
#     assert f.group == 'root'
#     assert host.run("httpd -t")


def test_httpd_config(host):
     assert host.run("httpd -t")  

def test_httpd_service(host):
    service =host.service("httpd")
    assert service.is_running is False
    assert service.is_enabled is True

def test_os_release(host):
    assert host.file("/etc/os-release").contains("Rocky")

def test_sshd_inactive(host):
    assert host.service("sshd").is_running is False