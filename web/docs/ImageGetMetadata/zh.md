# 获取图像元数据 (Get Image Metadata)

此节点提取已附加到图像张量（Tensor）上的元数据。

## 输入

- **image** (图像): 要从中获取元数据的图像张量。

## 输出

- **metadata** (元数据): 附加在该图像上的元数据字符串。

> [!CAUTION]
> 此节点**仅支持**由 **Load Image (Metadata)** 或 **Set Image Metadata** 处理过的图像。它**无法**从 ComfyUI 原生的 **Load Image** 节点（v0.9.1 版本）加载的图像中提取元数据，因为原生节点不会将元数据附加到图像张量中。
