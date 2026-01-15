import os
import json

# Simple i18n helper for ComfyUI nodes
# It tries to detect the language or defaults to English

_translations = {
    "en": {
        "Category": "MetadataTools",
        "LoadImageWithMetadata": "Load Image (Metadata)",
        "SaveImageWithMetadata": "Save Image (Metadata)",
        "ImageSetMetadata": "Set Image Metadata",
        "ImageGetMetadata": "Get Image Metadata",
        "metadata": "metadata",
        "image": "image",
        "mask": "mask",
    },
    "zh": {
        "Category": "元数据工具",
        "LoadImageWithMetadata": "加载图像 (带元数据)",
        "SaveImageWithMetadata": "保存图像 (带元数据)",
        "ImageSetMetadata": "设置图像元数据",
        "ImageGetMetadata": "获取图像元数据",
        "metadata": "元数据",
        "image": "图像",
        "mask": "遮罩",
    },
}


def get_lang():
    # Placeholder for language detection
    # Could check an environment variable or a config file
    return os.environ.get("COMFYUI_LANG", "en").lower()


def t(key, default=None):
    lang = get_lang()
    if lang not in _translations:
        lang = "en"
    return _translations[lang].get(key, default if default is not None else key)
