import os
import json
from PIL import Image, PngImagePlugin
import numpy as np
import torch
import folder_paths


class LoadImageWithMetadata:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {"image": (sorted(files), {"image_upload": True})},
        }

    CATEGORY = "MetadataTools"

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "metadata")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)

        # Extract metadata
        metadata = {}
        if i.info:
            for k, v in i.info.items():
                metadata[k] = v

        metadata_str = json.dumps(metadata, indent=4)

        i = PngImagePlugin.PngImageFile(image_path)

        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        if "A" in i.getbands():
            mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        return (image, mask, metadata_str)


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
                "metadata_text": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "MetadataTools"

    def save_images(self, images, metadata_text, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
        )
        results = list()

        # Parse user provided metadata
        try:
            user_metadata = json.loads(metadata_text)
        except json.JSONDecodeError:
            user_metadata = {"UserMetadata": metadata_text}

        for image in images:
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = PngImagePlugin.PngInfo()

            # Add existing metadata (e.g. prompt, workflow)
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            # Add user metadata
            for k, v in user_metadata.items():
                if isinstance(v, str):
                    metadata.add_text(k, v)
                else:
                    metadata.add_text(k, json.dumps(v))

            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {"LoadImageWithMetadata": LoadImageWithMetadata, "SaveImageWithMetadata": SaveImageWithMetadata}

NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageWithMetadata": "Load Image (Metadata)", "SaveImageWithMetadata": "Save Image (Metadata)"}
