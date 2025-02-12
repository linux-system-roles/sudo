# Sudo

This role configures sudo.

## Requirements

This role is only supported on RHEL8+ and Fedora distributions.
Consider reading sudo documentation before setting it up.

### Collection requirements

The role requires external collections only for management of `rpm-ostree`
nodes. Please run the following command to install them if you need to manage
`rpm-ostree` nodes:

```bash
ansible-galaxy collection install -vv -r meta/collection-requirements.yml
```

## Role Variables

The defaults defined for this role are based on a default RHEL8.4 `/etc/sudoers` configuration.
Check the defaults in [`defaults/main.yml`](defaults/main.yml) prior to running for OS compatibility.

### sudo_rewrite_default_sudoers_file

Use role default or user defined `sudo_sudoers_files` definition, replacing your distribution supplied `/etc/sudoers` file.
Useful when attempting to deploy new configuration files to the `include_directories` and you do not wish to modify the `/etc/sudoers` file.

Default: `true`

Type: `bool`

### sudo_check_if_configured

This variable provides semantic check of already configured sudoers in case ansible setup is not needed and it is skipped.

Default: `true`

Type: `bool`

### sudo_remove_unauthorized_included_files

***Dangerous!*** Setting this to `true` removes each existing sudoers file in the `include_directories` dictionary that are not defined in the`sudo_sudoers_files` variable.
This allows for enforcing a desired state.

Default: `false`
Type: `bool`

### sudo_visudo_path

Fully-qualified path to the `visudo` binary required for validation of sudoers configuration changes
Added for Operating System compatibility.

Default: `/usr/bin/visudo`

Type: `string`

### sudo_transactional_update_reboot_ok

This variable is used to handle reboots required by transactional updates.
If a transactional update requires a reboot, the role will proceed with the
reboot if `sudo_transactional_update_reboot_ok` is set to `true`. If set
to `false`, the role will notify the user that a reboot is required, allowing
for custom handling of the reboot requirement. If this variable is not set,
the role will fail to ensure the reboot requirement is not overlooked.

Default: `null`
Type: `bool`

### sudo_sudoers_files

A list that defines sudoers configurations.

For the default configuration, see [defaults/main.yml](defaults/main.yml).

Type: `list`

#### path

Where to deploy the configuration file to on the filesystem.

Type: `string`

#### aliases

A dictionary containing optional definition of `User_Alias`, `Runas_Alias`, `Host_Alias`, and `Cmnd_Alias` aliases.

This dictionary can be used to assign either user specifications or default overrides.

Available keys:

1. `user_alias`, requires setting a name with the `name` string and a list of users with the `users` list.
2. `runas_alias`, requires setting a name with the `name` string and a list of users with the `users` list.
3. `host_alias`, requires setting a name with the `name` string and a list of hosts with the `hosts` list.
4. `cmnd_alias`, requires setting a name with the `name` string and a list of commands with the `commands` list.

Example definition:

```yaml
sudo_sudoers_files:
  aliases:
    user_alias:
      - name: PINGERS
        users:
          - username
    runas_alias:
      - name: RUNAS
        users:
          - username
    cmnd_alias:
      - name: PING
        commands:
          - /usr/bin/ping
    cmnd_alias:
      - name: PING
        commands:
          - /usr/bin/ping
```

#### defaults

You can use this to define the defaults of sudoers configuration.

You can perform default overrides via the [`user_specifications`](#default-override-user_specifications) key.

Type: `list`

#### include_files

Optional, a list of files that your configuration must include.

This is a list of fully-qualified paths to include via the `#include` option of a sudoers configuration.

Type: `list`

#### include_directories

Optional, a list of directories that your configurations must include.

This is a list of fully-qualified paths to directories to include via the `#includedir` option of a sudoers configuration.

Type: `list`

#### user_specifications

You can use this `list` variable to apply user specifications to a sudoers file configuration.

Supported entries:

1. `users` - List of users to apply the specification to.
You can use a `user_alias` name as well as user names.

2. `hosts` - List of hosts to apply the specification to.
You can use a defined `host_alias` name as well as host names.

3. `operators` - List of operators to apply the specification to.
You can use a defined `runas_alias` name as well as user names.

4. `selinux_role` - Optional selinux role to apply to the specification.

5. `selinux_type` - Optional selinux type to apply to the specification.

6. `solaris_privs` - Optional Solaris privset to apply to the specification.

7. `solaris_limitprivs` - Optional Solaris privset to apply to the specification.

8. `tags` - Optional list of tags to apply to the specification.

9. `commands` - List of commands to apply the specification to.
You can use a defined `cmnd_alias` name as well as commands.

Example definition:

```yaml
sudo_sudoers_files:
  - path: /etc/sudoers.d/pingers
    user_specifications:
      - users:
          - root
        hosts:
          - ALL
        operators:
          - ALL
        commands:
          - ALL
      - users:
          - "%wheel"
        hosts:
          - ALL
        operators:
          - ALL
        commands:
          - ALL
```

#### default_overrides

You can use this `list` variable to apply Default Override user_specifications to a sudoers file configuration.

Supported entries:

1. `defaults` - List of defaults to override from the main configuration.

2. `type` - Type of default to override, this affects the operator in the configuration ( host -> `@`, user -> `:`, command -> `!`, and runas -> `>`).
The type field can be one of the following values: `command`, `host`, `runas`, or `user`.

3. `commands` - Use when `type: command`.
List of `cmnd_alias` names as well as commands to override specific default values.

4. `hosts` - Use when `type: host`.
List of `host_alias` names as well as individual host names to override specific default values.

5. `operators` - Use when `type: runas`.
List of `runas_alias` names as well as individual user names to override specific default values.

6. `users` - Use when `type: user`.
List of `user_alias` names as well as individual user names to override specific default values.

Example Definition:

```yaml
sudo_sudoers_files:
  - path: /etc/sudoers.d/pingers
    default_overrides:
      - type: user
        defaults:
          - "!requiretty"
        users:
          - PINGERS
      - type: runas
        defaults:
          - "!set_logname"
        operators:
          - root
      - type: host
        defaults:
          - "!requiretty"
          - "!requiretty"
        hosts:
          - host1
          - host2
      - type: command
        defaults:
          - "!requiretty"
        commands:
          - /usr/bin/ls
```

## Example Playbooks

### Applying a RHEL Default /etc/sudoers configuration

```yaml
---
- name: Apply a RHEL Default /etc/sudoers configuration
  hosts: all
  roles:
    - role: linux-system-roles.sudo
```

### Applying custom /etc/sudoers configuration

```yaml
---
- name: Apply a custom /etc/sudoers configuration
  hosts: all
  vars:
    sudoers_files:
      - path: /etc/sudoers
        user_specifications:
          - users:
              - root
            hosts:
              - x
            commands:
              - /usr/bin/ls
  roles:
    - role: linux-system-roles.sudo
```

### Applying defaults

```yaml
---
- name: Apply defaults
  hosts: all
  vars:
  sudoers_files:
    - path: /etc/sudoers
      defaults:
        - "!visiblepw"
        - always_set_home
        - match_group_by_gid
        - always_query_group_plugin
        - env_reset
        - secure_path:
          - /sbin
          - /bin
          - /usr/sbin
          - /usr/bin
        - env_keep:
          - COLORS
          - DISPLAY
          - HOSTNAME
          - HISTSIZE
          - KDEDIR
          - LS_COLORS
          - MAIL
          - PS1
          - PS2
          - QTDIR
          - USERNAME
          - LANG
          - LC_ADDRESS
          - LC_CTYPE
          - LC_COLLATE
          - LC_IDENTIFICATION
          - LC_MEASUREMENT
          - LC_MESSAGES
          - LC_MONETARY
          - LC_NAME
          - LC_NUMERIC
          - LC_PAPER
          - LC_TELEPHONE
          - LC_TIME
          - LC_ALL
          - LANGUAGE
          - LINGUAS
          - _XKB_CHARSET
          - XAUTHORITY
      user_specifications:
        - users:
            - root
          hosts:
            - ALL
          operators:
            - ALL
          commands:
            - ALL
        - users:
            - "%wheel"
          hosts:
            - ALL
          operators:
            - ALL
          commands:
            - ALL
      include_directories:
        - /etc/sudoers.d
  roles:
    - role: linux-system-roles.sudo
```

### Applying a multi-file sudoers configuration

```yaml
---
- name: Apply a multi-file sudoers configuration
  hosts: all
  tasks:
    - name: Configure /etc/sudoers and included files
      include_role:
        name: linux-system-roles.sudo
      vars:
        sudo_rewrite_default_sudoers_file: true
        sudo_remove_unauthorized_included_files: true
        sudo_sudoers_files:
          - path: /etc/sudoers
            defaults:
              - "!visiblepw"
              - always_set_home
              - match_group_by_gid
              - always_query_group_plugin
              - env_reset
              - secure_path:
                - /sbin
                - /bin
                - /usr/sbin
                - /usr/bin
              - env_keep:
                - COLORS
                - DISPLAY
                - HOSTNAME
                - HISTSIZE
                - KDEDIR
                - LS_COLORS
                - MAIL
                - PS1
                - PS2
                - QTDIR
                - USERNAME
                - LANG
                - LC_ADDRESS
                - LC_CTYPE
                - LC_COLLATE
                - LC_IDENTIFICATION
                - LC_MEASUREMENT
                - LC_MESSAGES
                - LC_MONETARY
                - LC_NAME
                - LC_NUMERIC
                - LC_PAPER
                - LC_TELEPHONE
                - LC_TIME
                - LC_ALL
                - LANGUAGE
                - LINGUAS
                - _XKB_CHARSET
                - XAUTHORITY
            user_specifications:
              - users:
                  - root
                hosts:
                  - ALL
                operators:
                  - ALL
                commands:
                  - ALL
              - users:
                  - "%wheel"
                hosts:
                  - ALL
                operators:
                  - ALL
                commands:
                  - ALL
            include_directories:
              - /etc/sudoers.d
            aliases:
              cmnd_alias:
                - name: PING
                  commands:
                    - /usr/bin/ping
              user_alias:
                - name: PINGERS
                  users:
                    - username
          - path: /etc/sudoers.d/pingers
            user_specifications:
            - type: user
              defaults:
                - "!requiretty"
              users:
                - PINGERS
          - path: /etc/sudoers.d/root
            defaults:
              - syslog=auth
            user_specifications:
              - type: runas
                defaults:
                  - "!set_logname"
                operators:
                  - root
```

## rpm-ostree

See README-ostree.md

## License

MIT

Based on [Ansible-sudoers](https://github.com/ahuffman/ansible-sudoers).
[![ansible-lint.yml](https://github.com/linux-system-roles/sudo/actions/workflows/ansible-lint.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/ansible-lint.yml) [![ansible-test.yml](https://github.com/linux-system-roles/sudo/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/ansible-test.yml) [![codeql.yml](https://github.com/linux-system-roles/sudo/actions/workflows/codeql.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/codeql.yml) [![codespell.yml](https://github.com/linux-system-roles/sudo/actions/workflows/codespell.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/codespell.yml) [![markdownlint.yml](https://github.com/linux-system-roles/sudo/actions/workflows/markdownlint.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/markdownlint.yml) [![python-unit-test.yml](https://github.com/linux-system-roles/sudo/actions/workflows/python-unit-test.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/python-unit-test.yml) [![shellcheck.yml](https://github.com/linux-system-roles/sudo/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/shellcheck.yml) [![tft.yml](https://github.com/linux-system-roles/sudo/actions/workflows/tft.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/tft.yml) [![tft_citest_bad.yml](https://github.com/linux-system-roles/sudo/actions/workflows/tft_citest_bad.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/tft_citest_bad.yml) [![woke.yml](https://github.com/linux-system-roles/sudo/actions/workflows/woke.yml/badge.svg)](https://github.com/linux-system-roles/sudo/actions/workflows/woke.yml)
