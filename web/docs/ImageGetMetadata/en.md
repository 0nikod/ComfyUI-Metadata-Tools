# Get Image Metadata

This node retrieves metadata that has been attached to an image tensor.

## Inputs

- **image**: The image tensor to retrieve metadata from.

## Outputs

- **metadata**: The attached metadata as a string.

> [!CAUTION]
> This node **only** works with images processed by **Load Image (Metadata)** or **Set Image Metadata**. It **cannot** retrieve metadata from images loaded with the native ComfyUI **Load Image** node (v0.9.1), as the native node does not attach metadata to the image tensor.
