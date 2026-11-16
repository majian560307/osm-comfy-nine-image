# -*- coding: utf-8 -*-
"""OSM 九图分发器：9 个图片装载位（每个自带上传按钮），9 路 IMAGE 输出。

装载位选了文件 → 原样传递 IMAGE 张量到对应编号输出口；
装载位选了 "(未加载)" → 该输出口返回 ExecutionBlocker，
下游整条分支被内核视为死分支跳过，不执行、不报错、不影响其余分支。
"""
import os
import folder_paths
from comfy_execution.graph_utils import ExecutionBlocker
from nodes import LoadImage

NONE = "(未加载)"
N = 9


def _files():
    input_dir = folder_paths.get_input_directory()
    try:
        raw = [f for f in os.listdir(input_dir)
               if os.path.isfile(os.path.join(input_dir, f))]
    except OSError:
        raw = []
    return [NONE] + folder_paths.filter_files_content_types(raw, ["image"])


class OSMNineImageBranch:
    def __init__(self):
        self._loader = LoadImage()

    @classmethod
    def INPUT_TYPES(cls):
        # 每个槽位独立列出，前端才会渲染成 9 个独立的下拉+上传控件
        req = {}
        files = _files()
        for i in range(1, N + 1):
            req[f"img_{i}"] = (files, {"image_upload": True,
                                       "tooltip": f"槽位{i}：选图片则 {i} 号口输出 IMAGE；选“(未加载)”则下游整条分支跳过。"})
        return {"required": req}

    CATEGORY = "OSM"
    ESSENTIALS_CATEGORY = "Basics"
    DESCRIPTION = "9 位图片装载分发：空槽位的下游分支自动整体屏蔽。"
    RETURN_TYPES = ("IMAGE",) * N
    RETURN_NAMES = tuple(f"{i}" for i in range(1, N + 1))
    OUTPUT_IS_LIST = (False,) * N
    FUNCTION = "dispatch"

    def dispatch(self, **kw):
        out = []
        for i in range(1, N + 1):
            name = kw.get(f"img_{i}", NONE)
            if not name or name == NONE:
                out.append(ExecutionBlocker(f"槽位{i}未装载图片，分支屏蔽"))
            else:
                img, _mask = self._loader.load_image(name)
                out.append(img)
        return tuple(out)


class OSMNineImageBranchInput(OSMNineImageBranch):
    """连线模式：9 路 IMAGE 输入直连原生 LoadImage。
    上游喂 1x1 黑图 = 该槽视为空 → 对应编号输出的下游整条分支屏蔽。"""

    @classmethod
    def INPUT_TYPES(cls):
        opt = {}
        for i in range(1, N + 1):
            opt[f"img_{i}"] = ("IMAGE", {"tooltip": f"槽位{i}：接原生 LoadImage；喂 1x1 黑图 = 空槽，下游分支自动屏蔽。"})
        return {"required": {}, "optional": opt}

    DESCRIPTION = "9 路 IMAGE 输入分发：1x1 黑图占位视为空槽，下游分支自动屏蔽。配合 RH/云端应用的必填原生 LoadImage 使用。"

    @staticmethod
    def _is_placeholder(img):
        # 1x1 任意图，或 1x1 大小的任何像素 → 占位
        if img is not None and img.ndim >= 2 and img.shape[-3] == 1 and img.shape[-2] == 1:
            return True
        # 宽容：小尺寸(<8px)且全黑的图也判占位
        try:
            if img is not None and img.numel() > 0 and img.numel() <= 8 * 8 * 3 and float(img.abs().max()) == 0.0:
                return True
        except Exception:
            pass
        return False

    def dispatch(self, **kw):
        out = []
        for i in range(1, N + 1):
            img = kw.get(f"img_{i}", None)
            if img is None or self._is_placeholder(img):
                out.append(ExecutionBlocker(f"槽位{i}为 1x1 黑图占位，分支屏蔽"))
            else:
                out.append(img)
        return tuple(out)


NODE_CLASS_MAPPINGS = {
    "OSMNineImageBranch": OSMNineImageBranch,
    "OSMNineImageBranchInput": OSMNineImageBranchInput,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OSMNineImageBranch": ("OSM 九图分发器 (9槽·空槽自动屏蔽)"),
    "OSMNineImageBranchInput": ("OSM 九图分发器·连线版 (1x1黑图=空)"),
}
