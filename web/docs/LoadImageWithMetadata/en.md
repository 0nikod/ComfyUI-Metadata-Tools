# Load Image (Metadata)

This node loads an image from the input folder and extracts all its metadata (PNG info, etc.) as a JSON string.

> [!IMPORTANT]
> Unlike the native **Load Image** node (as of ComfyUI v0.9.1), this node explicitly extracts and provides metadata as an output, which is required for using the **Get Image Metadata** node.

## Inputs

- **image**: Select an image from the ComfyUI input directory.

## Outputs

- **image**: The loaded image.
- **mask**: The alpha channel of the image as a mask (if available).
- **metadata**: All extracted metadata formatted as a JSON string.

## Usage

This node is useful for inspecting the generation parameters or other metadata stored within an image file. The output string can be passed to other nodes for processing or display.
