"""Top-level package for comfyui_metadata_tools."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

from .src.comfyui_metadata_tools.nodes import NODE_CLASS_MAPPINGS
from .src.comfyui_metadata_tools.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
