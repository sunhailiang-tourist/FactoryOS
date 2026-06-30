"""license_service 包入口。

作用：Pack 授权校验公开 API。
业务关联：T-02 execution 门禁 · W6 stub。
上游：execution_service（Step2）
下游：tenant 静态 licensed 列表（W6 stub）
"""
from __future__ import annotations

from os_core.license_service.service import assert_pack_licensed, is_pack_licensed

__all__ = ["assert_pack_licensed", "is_pack_licensed"]
