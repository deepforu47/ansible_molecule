import http
import unittest
import os
import pytest
from subprocess_tee import run
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_httpd_config(host):
     assert host.run("httpd -t")  

def test_httpd_service(host):
    service =host.service("httpd")
    assert service.is_running is True
    assert service.is_enabled is True

def test_os_release(host):
    assert host.file("/etc/os-release").contains("Rocky")
