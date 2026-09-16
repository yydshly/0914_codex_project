# Mermaid IR — research.mmd

1 diagram(s): [0] flowchart (6n/5e)

## Diagram 0 — flowchart

- source layout: none (Mermaid is layout-free); direction: LR
- nodes: 6 total / 6 drawable / 0 containers, depth 0
- edges: 5 (0 labeled, 0 dangling), cycle: False
- shapes: {'rect': 6}
- type candidates: architecture
- budget: nodes ok (max 9), edges ok (max 12)
- hubs (focal candidates): 生成图形(2), 整理图规格(2), 核实事实(2), 提取关系(2), 检查与导出(1)
- entry points: 原始资料
- terminals: 检查与导出

### Nodes

| id | label | shape | depth | parent | deg | fields |
|---|---|---|---|---|---|---|
| n0 | 原始资料 | rect | 0 | - | 0/1 | - |
| n1 | 提取关系 | rect | 0 | - | 1/1 | - |
| n2 | 核实事实 | rect | 0 | - | 1/1 | - |
| n3 | 整理图规格 | rect | 0 | - | 1/1 | - |
| n4 | 生成图形 | rect | 0 | - | 1/1 | - |
| n5 | 检查与导出 | rect | 0 | - | 1/0 | - |

### Edges

| source | target | label | style |
|---|---|---|---|
| 原始资料 | 提取关系 | - | solid arrow |
| 提取关系 | 核实事实 | - | solid arrow |
| 核实事实 | 整理图规格 | - | solid arrow |
| 整理图规格 | 生成图形 | - | solid arrow |
| 生成图形 | 检查与导出 | - | solid arrow |
