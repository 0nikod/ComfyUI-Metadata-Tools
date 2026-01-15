# Set Image Metadata

This node attaches custom metadata to an image tensor. This metadata "travels" with the image and can be retrieved later or saved to a file.

## Inputs

- **image**: The image tensor to attach metadata to.
- **metadata**: The string or JSON metadata to attach.

## Outputs

- **image**: The image tensor with the metadata attached as an internal attribute.

## Usage

This node is useful for tagging images with custom information during the workflow, which can then be used by the **Save Image (Metadata)** node to save that information into the final PNG file.

> [!WARNING]
> Using the native ComfyUI **Save Image** node will cause the embedded workflow and prompt to overwrite any custom metadata attached by this node. To preserve your custom metadata in the saved file, you **must** use the **Save Image (Metadata)** node provided by this plugin.
