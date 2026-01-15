"""Top-level package for comfyui_metadata_tools."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

__author__ = """ComfyUI-Metadata-Tools"""
__email__ = "dniko0@outlook.com"
__version__ = "0.0.1"

from .src.comfyui_metadata_tools.nodes import NODE_CLASS_MAPPINGS
from .src.comfyui_metadata_tools.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
