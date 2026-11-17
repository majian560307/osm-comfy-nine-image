# OSM Comfy Nine Image Branch / OSM 九图分发器

Two ComfyUI nodes — **9 image slots, 9 numbered IMAGE outputs**, empty slots handled automatically.
两个 ComfyUI 节点——**9 装载位 + 9 路编号 IMAGE 输出**，空槽自动处理。

## Variants / 两个变体

### 1. `OSMNineImageBranch` — 自带上传版
9 dropdown slots each with its own upload button; empty = `(未加载)` → downstream branch **pruned** by kernel `ExecutionBlocker`.
9 个独立下拉+上传按钮；空槽 → 下游整条分支被内核 `ExecutionBlocker` 屏蔽。适合本地 ComfyUI。

### 2. `OSMNineImageBranchInput` — 连线版（为 RH/云端应用设计）
9 optional `IMAGE` inputs wired from native Load Image nodes. A slot counts as **empty** when unconnected or fed a 1x1/black placeholder. The `empty_mode` switch decides what happens downstream:
9 路可选 IMAGE 输入接原生 LoadImage。未连线或喂入 1x1/纯黑占位图 = **空槽**。`empty_mode` 开关决定下游行为：

- **`black`（默认）** — empty slots pass a synthesized 1x1 black IMAGE downstream. Use when the downstream node (e.g. H3 multi-image loader) **requires** every input to be an image and errors on missing inputs.
  空槽自动向后传一张合成 1x1 黑图。当下游（如 H3 多图加载节点）强制要求每个输入必须有图、缺图报错时使用。
- **`block`** — empty slots return `ExecutionBlocker`; the entire downstream branch is skipped. Use when downstream inputs are optional.
  空槽返回 `ExecutionBlocker`，下游整条分支跳过执行。下游输入可选时使用。

## Install / 安装

```
cd ComfyUI/custom_nodes
git clone https://github.com/majian560307/osm-comfy-nine-image.git osm_nine_image_branch
```

Restart ComfyUI → Add Node → search `九图` (category `OSM`).
For the wired variant you may also drop `placeholder_1x1_black.png` into `ComfyUI/input/` as the native Load Image default (must be RGB PNG — v0.44's pyav loader rejects gray exotic PNGs).
连线版可将 `placeholder_1x1_black.png` 放入 `ComfyUI/input/` 作为原生 LoadImage 默认值（须 RGB PNG）。

## Verified / 已验证

Local ComfyUI v0.44 + RunningHub: black mode → all 9 outputs fed (real images pass, empties get 1x1 black), prompt success; block mode → only real-image branches execute.
本机 v0.44 与 RH 均实测：black 模式 9 口全有图（实图透传、空槽补 1x1 黑）；block 模式仅实图分支执行。

## License

MIT
