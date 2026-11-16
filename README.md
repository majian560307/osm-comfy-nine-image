# OSM Comfy Nine Image Branch / OSM 九图分发器

A ComfyUI custom node with **9 image loader slots** and **9 numbered IMAGE outputs**.

一个 ComfyUI 自定义节点：**9 个图片装载位** + **9 路按编号 1~9 的 IMAGE 输出口**。

## Behavior / 行为

- Slot has an image selected → the corresponding output passes the `IMAGE` tensor straight through.
  装载位选了图片 → 对应编号输出口原样传递 IMAGE 张量。
- Slot is `(未加载)` (not loaded) → that output returns a kernel `ExecutionBlocker`, so the **entire downstream branch is skipped** by ComfyUI's executor: no error, no placeholder, no impact on other branches.
  装载位留 `(未加载)` → 该输出口返回内核 `ExecutionBlocker`，**下游整条分支被执行器屏蔽**：不报错、不占位、不影响其余分支执行。

Each slot is an independent dropdown with its own upload button (same UX as the built-in Load Image node).
每个装载位都是独立下拉框 + 自带上传按钮（与原生 Load Image 相同交互）。

## Install / 安装

```
cd ComfyUI/custom_nodes
git clone https://github.com/majian560307/osm-comfy-nine-image.git osm_nine_image_branch
```

Restart ComfyUI, then right-click canvas → Add Node → search `九图` or `OSMNineImageBranch` (category: `OSM`).

重启 ComfyUI，右键画布 → Add Node → 搜索「九图」或 `OSMNineImageBranch`（分类 OSM）。

## Note / 注意

A downstream node is only skipped when **all** of its execution paths originate from blocked slots. If a node links both a loaded slot and an empty slot, it still runs (fed by the loaded one).

死分支跳过的前提：该节点的所有执行路径都来自空槽口。若某节点同时连了有图的槽和空槽，它仍会执行。

## License

MIT
