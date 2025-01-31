# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Radovan Sroka <rsroka@redhat.com>
# SPDX-License-Identifier: GPL-2.0-or-later
#
"""Unit tests for the scan_sudoers module"""


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import unittest

try:
    from unittest.mock import patch, mock_open
except ImportError:
    from mock import patch, mock_open


from scan_sudoers import get_includes, get_user_specs, get_config_lines

from pprint import pprint

if sys.version_info[0] < 3:
    open_path = "__builtin__.open"  # Python 2.7
else:
    open_path = "builtins.open"  # Python 3+


class TestScanSudoers(unittest.TestCase):

    @patch("scan_sudoers.os.listdir")
    @patch("scan_sudoers.isfile")
    @patch(
        open_path,
        new_callable=mock_open,
        read_data="#includedir /etc/sudoers.d\n",
    )
    def test_get_includes01(self, mock_open, mock_isfile, mock_listdir):
        # Arrange
        mock_isfile.return_value = True
        mock_listdir.return_value = ["file1", "file2"]
        expected_output = {
            "include_directories": ["/etc/sudoers.d"],
            "include_files": ["/etc/sudoers.d/file1", "/etc/sudoers.d/file2"],
        }

        # Act
        result = get_includes("/etc/sudoers")

        print(result)
        # Assert
        self.assertEqual(result, expected_output)
        mock_open.assert_called_once_with("/etc/sudoers", "r")
        mock_isfile.assert_called()
        mock_listdir.assert_called_once_with("/etc/sudoers.d")

    @patch("scan_sudoers.os.listdir")
    @patch("scan_sudoers.isfile")
    @patch(
        open_path,
        new_callable=mock_open,
        read_data="#include /etc/sudoers.d/file1\n#include /etc/sudoers.d/file2\n",
    )
    def test_get_includes02(self, mock_open, mock_isfile, mock_listdir):
        # Arrange
        mock_isfile.return_value = True
        mock_listdir.return_value = ["file1", "file2"]
        expected_output = {
            "include_files": ["/etc/sudoers.d/file1", "/etc/sudoers.d/file2"]
        }

        # Act
        result = get_includes("/etc/sudoers2")

        print(result)
        # Assert
        self.assertEqual(result, expected_output)
        mock_open.assert_called_once_with("/etc/sudoers2", "r")

    def test_get_user_specs03(self):
        # Arrange
        expected_output = {
            "users": ["%wheel"],
            "hosts": ["ALL"],
            "operators": ["ALL"],
            "tags": ["NOPASSWD"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("%wheel ALL=(ALL) NOPASSWD: ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs04(self):
        # Arrange
        expected_output = {
            "users": ["username1"],
            "hosts": ["ALL"],
            "operators": ["ALL"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("username1 ALL=(ALL) ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs05(self):
        # Arrange
        expected_output = {
            "users": ["username2"],
            "hosts": ["hostname"],
            "operators": ["runas_user:runas_group"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("username2 hostname=(runas_user:runas_group)  ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs06(self):
        # Arrange
        expected_output = {
            "users": ["john"],
            "hosts": ["ALL"],
            "operators": ["ALL:ALL"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("john ALL=(ALL:ALL) ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs07(self):
        # Arrange
        expected_output = {
            "users": ["jane"],
            "hosts": ["ALL"],
            "operators": ["ALL:ALL"],
            "tags": ["NOPASSWD"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("jane ALL=(ALL:ALL) NOPASSWD: ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs08(self):
        # Arrange
        expected_output = {
            "users": ["developer"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "commands": ["/usr/bin/systemctl", "/usr/bin/journalctl"],
        }

        # Act
        result = get_user_specs(
            "developer ALL=(root:ALL) /usr/bin/systemctl, /usr/bin/journalctl"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs09(self):
        # Arrange
        expected_output = {
            "users": ["%admins"],
            "hosts": ["ALL"],
            "operators": ["ALL:ALL"],
            "commands": ["ALL"],
        }

        # Act
        result = get_user_specs("%admins ALL=(ALL:ALL) ALL")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs10(self):
        # Arrange
        expected_output = {
            "users": ["deploy"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "tags": ["NOPASSWD"],
            "commands": ["/usr/sbin/service apache2 restart"],
        }

        # Act
        result = get_user_specs(
            "deploy ALL=(root:ALL) NOPASSWD: /usr/sbin/service apache2 restart"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs11(self):
        # Arrange
        expected_output = {
            "users": ["backup"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "commands": ["/bin/tar", "/usr/bin/rsync"],
        }

        # Act
        result = get_user_specs("backup ALL=(root:ALL) /bin/tar, /usr/bin/rsync")
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs12(self):
        # Arrange
        expected_output = {
            "users": ["sysadmin"],
            "hosts": ["ALL"],
            "operators": ["ALL:ALL"],
            "commands": ["/usr/sbin/ifconfig", "/sbin/reboot", "/sbin/shutdown"],
        }

        # Act
        result = get_user_specs(
            "sysadmin ALL=(ALL:ALL) /usr/sbin/ifconfig, /sbin/reboot, /sbin/shutdown"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs13(self):
        # Arrange
        expected_output = {
            "users": ["dbadmin"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "tags": ["NOPASSWD"],
            "commands": ["/usr/sbin/service mysql restart", "/usr/bin/mysqladmin"],
        }

        # Act
        result = get_user_specs(
            "dbadmin ALL=(root:ALL) NOPASSWD: /usr/sbin/service mysql restart, /usr/bin/mysqladmin"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs14(self):
        # Arrange
        expected_output = {
            "users": ["audit"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "commands": ["/usr/bin/journalctl", "/bin/dmesg", "/usr/bin/uptime"],
        }

        # Act
        result = get_user_specs(
            "audit ALL=(root:ALL) /usr/bin/journalctl, /bin/dmesg, /usr/bin/uptime"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    def test_get_user_specs15(self):
        # Arrange
        expected_output = {
            "users": ["%devops"],
            "hosts": ["ALL"],
            "operators": ["root:ALL"],
            "commands": [
                "/usr/bin/docker ps",
                "/usr/bin/docker exec",
                "/usr/bin/docker logs",
            ],
        }

        # Act
        result = get_user_specs(
            "%devops ALL=(root:ALL) /usr/bin/docker ps, /usr/bin/docker exec, /usr/bin/docker logs"
        )
        print(result)
        print(expected_output)

        # Assert
        self.assertEqual(result, expected_output)

    @patch(
        open_path,
        new_callable=mock_open,
        read_data="""
#includedir /etc/sudoers.d
Cmnd_Alias MY_CMDS = /bin/ls, /bin/cat
Defaults env_keep += \"COLORS DISPLAY\"
%wheel ALL=(ALL) NOPASSWD: ALL
""",
    )
    @patch(
        "scan_sudoers.get_includes",
        return_value={"include_files": ["/etc/sudoers.d/file1"]},
    )
    def test_get_config_lines01(self, mock_open, mock_get_includes):
        # Arrange

        params = {"output_raw_configs": True, "output_parsed_configs": True}
        expected_output = {
            "path": "/etc/sudoers10",
            "configuration": [
                "#includedir /etc/sudoers.d",
                "Cmnd_Alias MY_CMDS = /bin/ls, /bin/cat",
                'Defaults env_keep += "COLORS DISPLAY"',
                "%wheel ALL=(ALL) NOPASSWD: ALL",
            ],
            "include_files": ["/etc/sudoers.d/file1"],
            "aliases": {
                "cmnd_alias": [{"commands": ["/bin/ls", "/bin/cat"], "name": "MY_CMDS"}]
            },
            "defaults": [{"env_keep": ["COLORS", "DISPLAY"]}],
            "user_specifications": [
                {
                    "commands": ["ALL"],
                    "hosts": ["ALL"],
                    "operators": ["ALL"],
                    "tags": ["NOPASSWD"],
                    "users": ["%wheel"],
                }
            ],
        }
        # Act
        result = get_config_lines("/etc/sudoers10", params)
        pprint(result)
        pprint(expected_output)

        # Assert
        self.assertEqual(result["configuration"], expected_output["configuration"])
        self.assertEqual(result["include_files"], expected_output["include_files"])
        self.assertEqual(result, expected_output)

    @patch(
        open_path,
        new_callable=mock_open,
        read_data="""
#includedir /etc/sudoers.d
Host_Alias WEBSERVERS = web1, web2, web3
Host_Alias DB_SERVERS = db1, db2
User_Alias ADMINS = john, jane, %sysadmins
User_Alias DEVS = deploy, dev, %developers
User_Alias DBAS = %db_team
Cmnd_Alias DB_CMDS = /usr/bin/mysql, /usr/bin/psql
Cmnd_Alias NETWORK_CMDS = /sbin/ifconfig, /sbin/ip
Cmnd_Alias SYSTEM_CMDS = /usr/bin/top, /usr/bin/htop, /usr/bin/uptime
ADMINS ALL=(ALL:ALL) ALL
DEVS WEBSERVERS=(root:ALL) NOPASSWD: APACHE_CMDS, NGINX_CMDS
DBAS DB_SERVERS=(root:ALL) NOPASSWD: DB_CMDS
netops ALL=(root:ALL) NOPASSWD: NETWORK_CMDS
monitor ALL=(ALL:ALL) SYSTEM_CMDS
""",
    )
    @patch(
        "scan_sudoers.get_includes",
        return_value={"include_files": ["/etc/sudoers.d/file1"]},
    )
    def test_get_config_lines02(self, mock_open, mock_get_includes):
        # Arrange
        params = {"output_raw_configs": True, "output_parsed_configs": True}
        expected_output = {
            "path": "/etc/sudoers10",
            "configuration": [
                "#includedir /etc/sudoers.d",
                "Host_Alias WEBSERVERS = web1, web2, web3",
                "Host_Alias DB_SERVERS = db1, db2",
                "User_Alias ADMINS = john, jane, %sysadmins",
                "User_Alias DEVS = deploy, dev, %developers",
                "User_Alias DBAS = %db_team",
                "Cmnd_Alias DB_CMDS = /usr/bin/mysql, /usr/bin/psql",
                "Cmnd_Alias NETWORK_CMDS = /sbin/ifconfig, /sbin/ip",
                "Cmnd_Alias SYSTEM_CMDS = /usr/bin/top, /usr/bin/htop, /usr/bin/uptime",
                "ADMINS ALL=(ALL:ALL) ALL",
                "DEVS WEBSERVERS=(root:ALL) NOPASSWD: APACHE_CMDS, NGINX_CMDS",
                "DBAS DB_SERVERS=(root:ALL) NOPASSWD: DB_CMDS",
                "netops ALL=(root:ALL) NOPASSWD: NETWORK_CMDS",
                "monitor ALL=(ALL:ALL) SYSTEM_CMDS",
            ],
            "include_files": ["/etc/sudoers.d/file1"],
            "aliases": {
                "cmnd_alias": [
                    {
                        "name": "DB_CMDS",
                        "commands": ["/usr/bin/mysql", "/usr/bin/psql"],
                    },
                    {
                        "name": "NETWORK_CMDS",
                        "commands": ["/sbin/ifconfig", "/sbin/ip"],
                    },
                    {
                        "name": "SYSTEM_CMDS",
                        "commands": [
                            "/usr/bin/top",
                            "/usr/bin/htop",
                            "/usr/bin/uptime",
                        ],
                    },
                ],
                "host_alias": [
                    {"hosts": ["web1", "web2", "web3"], "name": "WEBSERVERS"},
                    {"hosts": ["db1", "db2"], "name": "DB_SERVERS"},
                ],
                "user_alias": [
                    {"name": "ADMINS", "users": ["john", "jane", "%sysadmins"]},
                    {"name": "DEVS", "users": ["deploy", "dev", "%developers"]},
                    {"name": "DBAS", "users": ["%db_team"]},
                ],
            },
            "user_specifications": [
                {
                    "users": ["ADMINS"],
                    "hosts": ["ALL"],
                    "operators": ["ALL:ALL"],
                    "commands": ["ALL"],
                },
                {
                    "users": ["DEVS"],
                    "hosts": ["WEBSERVERS"],
                    "operators": ["root:ALL"],
                    "commands": ["APACHE_CMDS", "NGINX_CMDS"],
                    "tags": ["NOPASSWD"],
                },
                {
                    "users": ["DBAS"],
                    "hosts": ["DB_SERVERS"],
                    "operators": ["root:ALL"],
                    "commands": ["DB_CMDS"],
                    "tags": ["NOPASSWD"],
                },
                {
                    "users": ["netops"],
                    "hosts": ["ALL"],
                    "operators": ["root:ALL"],
                    "commands": ["NETWORK_CMDS"],
                    "tags": ["NOPASSWD"],
                },
                {
                    "users": ["monitor"],
                    "hosts": ["ALL"],
                    "operators": ["ALL:ALL"],
                    "commands": ["SYSTEM_CMDS"],
                },
            ],
        }
        # Act
        result = get_config_lines("/etc/sudoers10", params)
        # pprint(result)
        # Assert
        self.assertEqual(result["configuration"], expected_output["configuration"])
        self.assertEqual(result["include_files"], expected_output["include_files"])
        self.assertEqual(
            result["user_specifications"], expected_output["user_specifications"]
        )
        self.assertEqual(result["aliases"], expected_output["aliases"])
        # self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
