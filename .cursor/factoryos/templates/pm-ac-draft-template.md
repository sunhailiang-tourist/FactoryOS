# PM AC 草案：<标题>

- **日期**：YYYY-MM-DD
- **口令**：`【PM模式启动】`
- **用途**：供 Dev 誊入 `plan-*.md` §AC 对账表；**不替代** `gate plan`

## 1. 验收套件映射

| 草案 ID | 标题 | 映射正式 AC | 套件 | 验证思路 |
|---------|------|-------------|------|----------|
| PM-AC-01 | | 如 STU-01 / G-01 / … | BASE/MVP/STU/UX | pytest / 手工 / Studio |

## 2. 人审 Gate 覆盖

| Gate | 本草案是否覆盖 | UI 动作 + Audit |
|------|----------------|-----------------|
| G-FREEZE | | |
| G-SHADOW | | |
| G-WRITE-APPROVE | | |

顺序必须：`G-FREEZE → G-SHADOW → G-WRITE-APPROVE`

## 3. 红线触点（若有）

| 红线 | 本草案负向点 |
|------|--------------|
| R-01～R-11 | |

## 4. 移交 Dev 备注

- plan 建议 Step 切分：
- 禁止项（实现时不可破）：
