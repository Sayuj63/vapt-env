# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Security Audit Environment — AI-powered VAPT training."""

# Pytest (and other tools) may import this file as a top-level module when the repo
# root is treated as a "package" path. Relative imports need a parent package; fall
# back to same-directory imports so `pytest` still works. Normal `import security_audit_env`
# from an install uses the relative branch.
try:
    from .client import SecurityAuditEnv
    from .models import (
        LLMJsonAction,
        SecurityAuditAction,
        SecurityAuditObservation,
        SecurityAuditState,
        extract_json_object_from_text,
        parse_llm_action_text,
    )
except ImportError:  # pragma: no cover
    from client import SecurityAuditEnv
    from models import (
        LLMJsonAction,
        SecurityAuditAction,
        SecurityAuditObservation,
        SecurityAuditState,
        extract_json_object_from_text,
        parse_llm_action_text,
    )

__all__ = [
    "LLMJsonAction",
    "SecurityAuditAction",
    "SecurityAuditObservation",
    "SecurityAuditState",
    "SecurityAuditEnv",
    "extract_json_object_from_text",
    "parse_llm_action_text",
]
