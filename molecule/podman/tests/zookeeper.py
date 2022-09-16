
import os
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('zookeeper')

# Confirm that specific packages and versions are installed
@pytest.mark.parametrize("name,version", [
    ("confluent-server", "7.2.1"),
])

def test_packages(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)

# Test that the cp-kafka user is available.
@pytest.mark.parametrize("user,group", [
    ("cp-kafka", "confluent"),
])
def test_users(host, user, group):
    usr = host.user(user)
    assert usr.exists
    assert usr.group == group

# Test that app.conf is present and has expected permissions
@pytest.mark.parametrize("filename,owner,group,mode", [
    ("/etc/kafka/zookeeper.properties", "cp-kafka", "confluent", 0o640),
])
def test_file(host, filename, owner, group, mode):
    target = host.file(filename)
    assert target.exists
    assert target.user == owner
    assert target.group == group
    assert target.mode == mode

def test_is_zookeeper_service_running(host):
    zookeeper_service = host.service('confluent-zookeeper.service')

    assert zookeeper_service.is_running
    assert zookeeper_service.is_enabled

def test_if_zookeeper_server_property_file_contains_configuration(host):
    server_property_file = host.file('/etc/kafka/zookeeper.properties')

    assert server_property_file.contains('dataDir=/var/lib/zookeeper')
    assert server_property_file.contains('dataLogDir=/opt/zookeeper')
