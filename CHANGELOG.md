Changelog
=========

[1.1.0] - 2024-08-01
--------------------

### New Features

- Handle reboot for transactional update systems (#16)

### Other Changes

- ci: Add tft plan and workflow (#14)
- ci: Update fmf plan to add a separate job to prepare managed nodes (#17)
- ci: bump sclorg/testing-farm-as-github-action from 2 to 3 (#18)

[1.0.1] - 2024-07-02
--------------------

### Bug Fixes

- fix: add support for EL10 (#12)

### Other Changes

- ci: ansible-lint action now requires absolute directory (#11)

[1.0.0] - 2024-06-11
--------------------

### Other Changes

- refactor: ostree support, simplify tests, lint issues (#5)
- ci: use tox-lsr 3.3.0 which uses ansible-test 2.17 (#6)
- ci: tox-lsr 3.4.0 - fix py27 tests; move other checks to py310 (#8)
- ci: Add supported_ansible_also to .ansible-lint (#9)

[0.1.0] - 2024-05-21
--------------------

### New Features

- feat: Add the sudo role (#2)

