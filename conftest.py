# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# Pytest: repo root is also the `security_audit_env` package. Without this,
# some pytest versions try to import `./__init__.py` as a test module, which
# fails (relative imports need a parent package). Keep this file free of
# `tests/` imports to avoid import cycles.

# Ignore the package entrypoint at repo root; actual tests live in tests/ only.
collect_ignore = ["__init__.py"]
