Changelog
=========

[1.2.6] - 2025-08-01
--------------------

### Bug Fixes

- fix: Use the correct regular expression to parse Cmnd_Alias and other aliases (#68)

[1.2.5] - 2025-07-09
--------------------

### Bug Fixes

- fix: ensure single space before TYPE, ROLE, and correctly format those values (#65)

[1.2.4] - 2025-06-23
--------------------

### Bug Fixes

- fix: Avoid setting ansible_managed variable (#61)
- fix: Avoid append() in sudoers file template (#62)

### Other Changes

- tests: Update tests_default.yml to do bootc end-to-end validation (#59)
- ci: Use ansible 2.19 for fedora 42 testing; support python 3.13 (#60)

[1.2.3] - 2025-05-21
--------------------

### Other Changes

- ci: ansible-plugin-scan is disabled for now (#36)
- ci: bump ansible-lint to v25; provide collection requirements for ansible-lint (#39)
- refactor: fix python black formatting (#40)
- ci: Check spelling with codespell (#41)
- ci: Add test plan that runs CI tests and customize it for each role (#42)
- ci: In test plans, prefix all relate variables with SR_ (#43)
- ci: Fix bug with ARTIFACTS_URL after prefixing with SR_ (#44)
- ci: Drop explicit "connection:" for provisioning (#45)
- ci: Run QEMU tox integration tests in GitHub workflow (#46)
- ci: Add Python 3.12 (#47)
- ci: several changes related to new qemu test, ansible-lint, python versions, ubuntu versions (#48)
- ci: use tox-lsr 3.6.0; improve qemu test logging (#50)
- ci: skip storage scsi, nvme tests in github qemu ci (#51)
- ci: Add container integration test for rpm and bootc (#52)
- ci: Update to tox-lsr 3.7.0 (#53)
- ci: bump sclorg/testing-farm-as-github-action from 3 to 4 (#54)
- ci: bump tox-lsr to 3.8.0; rename qemu/kvm tests (#55)
- ci: Add Fedora 42; use tox-lsr 3.9.0; use lsr-report-errors for qemu tests (#56)

[1.2.2] - 2025-01-09
--------------------

### Other Changes

- ci: bump codecov/codecov-action from 4 to 5 (#32)
- ci: Use Fedora 41, drop Fedora 39 (#33)
- ci: Use Fedora 41, drop Fedora 39 - part two (#34)

[1.2.1] - 2024-11-13
--------------------

### Other Changes

- refactor: role supports only EL8 and later - metadata should reflect that (#30)

[1.2.0] - 2024-10-30
--------------------

### New Features

- feat: Add variable that handles semantic check for sudoers (#22)

### Other Changes

- ci: Add workflow for ci_test bad, use remote fmf plan (#20)
- ci: Fix missing slash in ARTIFACTS_URL (#21)
- ci: Add python unit tests (#23)
- ci: Add tags to TF workflow, allow more [citest bad] formats (#24)
- ci: ansible-test action now requires ansible-core version (#25)
- ci: add YAML header to github action workflow files (#26)
- refactor: Use vars/RedHat_N.yml symlink for CentOS, Rocky, Alma wherever possible (#28)

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

