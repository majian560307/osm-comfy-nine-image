# OSM Comfy Nine Image Branch / OSM 九图分发器

Two ComfyUI nodes — **9 image slots, 9 numbered IMAGE outputs**, empty slots **prune their entire downstream branch** (kernel `ExecutionBlocker`, no error, no placeholder execution).

两个 ComfyUI 节点——**9 个装载位 + 9 路编号 IMAGE 输出**；空槽的**下游整条分支被内核 `ExecutionBlocker` 屏蔽**：不报错、不执行、不影响其余分支。

## Two variants / 两个变体

### 1. `OSMNineImageBranch` — 自带上传版
9 dropdown slots each with its own upload button (same UX as native Load Image). Empty = `(未加载)`.
9 个独立下拉+上传按钮，空槽 = `(未加载)`。适合本地 ComfyUI。

### 2. `OSMNineImageBranchInput` — 连线版（为 RH/云端应用设计）
9 optional `IMAGE` inputs; wire **native Load Image** nodes into them. **A 1x1 black placeholder image means "empty"** → that slot's downstream branch is pruned.
9 路可选 IMAGE 输入，接原生 LoadImage。**上游喂 1x1 黑图 = 该槽为空** → 对应分支屏蔽。

Why: cloud app hosts (e.g. RunningHub) only render upload widgets for native Load Image, and native Load Image **hard-fails validation when empty**. Feeding every slot keeps validation happy; the 1x1 sentinel carries the "empty" meaning instead.
原因：RH 等云平台只给原生 LoadImage 渲染上传控件，而原生 LoadImage 空值会直接触发运行前校验停止。全部喂图让校验永远通过，"空"的语义由 1x1 暗号承载。

## Setup for the wired variant / 连线版用法

1. Put `placeholder_1x1_black.png` (in this repo) into `ComfyUI/input/`.
   把本仓库的 `placeholder_1x1_black.png` 放进 `ComfyUI/input/`。
2. Add 9 native Load Image nodes; slots the user doesn't fill keep the placeholder as their value (set it as the node default).
   放 9 个原生 LoadImage；用户没传的槽保持默认 1x1 黑图。
3. Wire each LoadImage's IMAGE out into the matching `img_1..img_9` input; use outputs `1..9`.
   依编号连线，使用编号 1~9 输出口。

## Install / 安装

```
cd ComfyUI/custom_nodes
git clone https://github.com/majian560307/osm-comfy-nine-image.git osm_nine_image_branch
```

Restart ComfyUI → Add Node → search `九图` (category `OSM`).

## Verified / 已验证

Local ComfyUI v0.44: 9-loaded→9 run; 3 real + 6 placeholder→only 3; all-placeholder→none, prompt still success.
本包 v0.44 实测：全装 9 跑 9；3 实 6 占位只跑 3；全占位一个不跑且整图 success。
Note: placeholder must be an **RGB** PNG (v0.44's pyav loader rejects 1-bit/gray exotic PNGs). The bundled file is RGB.
注意：占位图须为 RGB PNG（新版 pyav 拒绝奇葩灰度格式），仓库自带文件已是 RGB。

## License

MIT
