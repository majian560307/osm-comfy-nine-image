# OSM Comfy Nine Image Branch / OSM 九图分发器

Three ComfyUI nodes — **9 image slots, 9 numbered IMAGE outputs**, empty slots handled automatically.
三个 ComfyUI 节点——**9 装载位 + 9 路编号 IMAGE 输出**，空槽自动处理。

## Nodes / 节点一览

| 节点 | 输入方式 | 空槽行为 | 适用 |
|---|---|---|---|
| `OSMNineImageBranch`<br>自带上传版 | 9 个自带下拉+上传按钮 | 下游整条分支屏蔽（`ExecutionBlocker`） | 本地 ComfyUI |
| `OSMNineImageBranchInput`<br>连线屏蔽版 | 9 路 IMAGE 输入接原生 LoadImage | 下游整条分支屏蔽 | 下游输入可选（RH 已支持无图上传时首选） |
| `OSMNineImageFillBlack`<br>连线补黑版 | 9 路 IMAGE 输入接原生 LoadImage | 输出口自动补传合成 1x1 黑图，下游 9 口永远有图 | 下游强制每口必须有图、缺图报错（如 H3 多图加载节点） |

连线版"空"的判定：输入口未连线，或上游喂的是 1x1 / 纯黑占位图（仓库自带 `placeholder_1x1_black.png`，须 RGB PNG——v0.44 pyav 拒收灰度异形 PNG）。

## Install / 安装

```
cd ComfyUI/custom_nodes
git clone https://github.com/majian560307/osm-comfy-nine-image.git osm_nine_image_branch
```

Restart ComfyUI → Add Node → search `九图` (category `OSM`).
连线版可将 `placeholder_1x1_black.png` 放入 `ComfyUI/input/` 作为原生 LoadImage 默认值。

## Verified / 已验证

Local ComfyUI v0.44 + RunningHub:
- 屏蔽版：3 实图输入 → 仅实图分支执行，空槽分支静默跳过；
- 补黑版：3 实图 + 空槽 → 9 口全有图、下游全执行、不报错；
- 自带上传版全空 → 不执行、不报错。

## License

MIT
