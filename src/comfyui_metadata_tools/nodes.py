import os
import json
from PIL import Image, PngImagePlugin
import numpy as np
import torch
import folder_paths
from .i18n import t


class LoadImageWithMetadata:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {"image": (sorted(files), {"image_upload": True})},
        }

    CATEGORY = t("Category")
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = (t("image"), t("mask"), t("metadata"))
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)

        # Extract metadata
        metadata = {}
        if img.info:
            for k, v in img.info.items():
                metadata[k] = v

        metadata_str = json.dumps(metadata, indent=4)

        # Process image
        output_image = img.convert("RGB")
        output_image = np.array(output_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_image)[None,]

        # Attach metadata to tensor for "traveling"
        setattr(output_image, "_metadata", metadata_str)

        # Process mask
        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        return (output_image, mask, metadata_str)


class SaveImageWithMetadata:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "metadata_text": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = t("Category")

    def save_images(self, images, metadata_text, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
        )
        results = list()

        for image in images:
            # Use provided text if not empty, otherwise check for attached attribute
            final_metadata_text = metadata_text
            if not final_metadata_text and hasattr(image, "_metadata"):
                final_metadata_text = getattr(image, "_metadata")

            # Parse metadata
            try:
                user_metadata = json.loads(final_metadata_text) if final_metadata_text else {}
            except json.JSONDecodeError:
                user_metadata = {"UserMetadata": final_metadata_text}

            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = PngImagePlugin.PngInfo()

            # Add existing metadata (e.g. prompt, workflow)
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            # Add user/attached metadata
            if isinstance(user_metadata, dict):
                for k, v in user_metadata.items():
                    val = v if isinstance(v, (str, int, float, bool)) else json.dumps(v)
                    metadata.add_text(str(k), str(val))
            else:
                metadata.add_text("Metadata", str(user_metadata))

            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
            counter += 1

        return {"ui": {"images": results}}


class ImageSetMetadata:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"image": ("IMAGE",), "metadata": ("STRING", {"multiline": True, "dynamicPrompts": False})},
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "set_metadata"
    CATEGORY = t("Category")

    def set_metadata(self, image, metadata):
        # Attach attribute to the tensor
        # Work on a copy if possible to avoid side effects?
        # Metadata is attached to the tensor itself.
        setattr(image, "_metadata", metadata)
        return (image,)


class ImageGetMetadata:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"image": ("IMAGE",)},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = (t("metadata"),)
    FUNCTION = "get_metadata"
    CATEGORY = t("Category")

    def get_metadata(self, image):
        metadata = getattr(image, "_metadata", "")
        return (metadata,)


NODE_CLASS_MAPPINGS = {
    "LoadImageWithMetadata": LoadImageWithMetadata,
    "SaveImageWithMetadata": SaveImageWithMetadata,
    "ImageSetMetadata": ImageSetMetadata,
    "ImageGetMetadata": ImageGetMetadata,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageWithMetadata": t("LoadImageWithMetadata"),
    "SaveImageWithMetadata": t("SaveImageWithMetadata"),
    "ImageSetMetadata": t("ImageSetMetadata"),
    "ImageGetMetadata": t("ImageGetMetadata"),
}
