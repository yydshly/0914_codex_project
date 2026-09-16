# Excalidraw IR — research\.excalidraw

1 scene: research (6n/5e)

## Scene — research

- source canvas: 1480×116 px (aspect 12.76)
- nodes: 6 total / 6 drawable / 0 containers, depth 0
- edges: 5 (0 labeled, 0 dangling), cycle: False
- shapes: {'rect': 6}
- type candidates: tree, architecture
- budget: nodes ok (max 9), edges ok (max 12)
- hubs (focal candidates): 提取关系(2), 核实事实(2), 整理图规格(2), 生成图形(2), 原始资料(1)
- entry points: 原始资料
- terminals: 检查与导出

### Nodes

| id | label | shape | depth | parent | deg | box |
|---|---|---|---|---|---|---|
| n0 | 原始资料 | rect | 0 | \- | 0/1 | 60,100 180×80 |
| n1 | 提取关系 | rect | 0 | \- | 1/1 | 320,136 180×80 |
| n2 | 核实事实 | rect | 0 | \- | 1/1 | 580,100 180×80 |
| n3 | 整理图规格 | rect | 0 | \- | 1/1 | 840,136 180×80 |
| n4 | 生成图形 | rect | 0 | \- | 1/1 | 1100,100 180×80 |
| n5 | 检查与导出 | rect | 0 | \- | 1/0 | 1360,136 180×80 |

### Edges

| source | target | label | style |
|---|---|---|---|
| 原始资料 | 提取关系 | - | - |
| 提取关系 | 核实事实 | - | - |
| 核实事实 | 整理图规格 | - | - |
| 整理图规格 | 生成图形 | - | - |
| 生成图形 | 检查与导出 | - | - |
