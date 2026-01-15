# Load Image (Metadata)

This node loads an image from the input folder and extracts all its metadata (PNG info, etc.) as a JSON string.

## Inputs

- **image**: Select an image from the ComfyUI input directory.

## Outputs

- **image**: The loaded image.
- **mask**: The alpha channel of the image as a mask (if available).
- **metadata**: All extracted metadata formatted as a JSON string.

## Usage

This node is useful for inspecting the generation parameters or other metadata stored within an image file. The output string can be passed to other nodes for processing or display.
