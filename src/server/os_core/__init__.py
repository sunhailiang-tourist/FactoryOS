"""FactoryOS 内核包根。

作用：标记 os_core 为可安装 Python 包。
业务关联：W1～W8 内核模块按 MODULE-MAP 落地。
上游：pytest · import 边界检查。
下游：os_core/*/service · shared_contracts。
"""

__all__: list[str] = []
