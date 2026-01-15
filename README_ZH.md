# ComfyUI 元数据工具 (Metadata Tools)

[简体中文](README_ZH.md) | [English](README.md)

一套用于 ComfyUI 的自定义节点，旨在高效处理图像元数据。此扩展允许您在工作流中直接提取、修改和保存元数据。

## 功能特点

- **元数据提取**: 加载图像并将其元数据（信息字典）作为 JSON 字符串输出。
- **自定义元数据保存**: 保存带有自定义元数据或从其他节点传递的元数据的图像。

## 节点说明

### 1. 加载图像 (带元数据) - Load Image (Metadata)
加载图像并输出：
- **IMAGE (图像)**: 图像张量。
- **MASK (遮罩)**: Alpha 通道（如果存在）。
- **metadata (元数据)**: 图像文件中发现的元数据，以 JSON 字符串形式呈现。

### 2. 保存图像 (带元数据) - Save Image (Metadata)
保存图像并允许添加自定义元数据：
- **images (图像)**: 要保存的图像。
- **metadata_text (元数据文本)**: (可选) 要保存为元数据的 JSON 字符串或纯文本。如果为空，则查找绑定在图像张量上的元数据。
- **filename_prefix (文件名路径)**: 保存文件的前缀。

### 3. 设置图像元数据 - Set Image Metadata
将元数据字符串附加到图像张量。如果没有提供显式文本，则“保存图像 (带元数据)”节点将使用此元数据。

### 4. 获取图像元数据 - Get Image Metadata
检索之前附加到图像张量的元数据字符串。

## 安装方法

1.  **ComfyUI-Manager (推荐)**:
    在 ComfyUI-Manager 中搜索 "Metadata Tools" 并点击安装。
2.  **手动安装**:
    ```bash
    cd ComfyUI/custom_nodes
    git clone https://github.com/dniko0/comfyui_metadata_tools
    cd comfyui_metadata_tools
    pip install -r requirements.txt
    ```

## 许可证

MIT
