"""Blueprint Runtime 包（W4 Step2 execute/entity）。

作用：重导出 runtime execute_op 入口。
业务关联：B-02 legacy_refs · C-02～C-04 entity mock。
上游：connector_sdk.registry
下游：runtime.entity · mock_legacy
"""
from os_core.connector_sdk.runtime.execute import execute_op

__all__ = ["execute_op"]
