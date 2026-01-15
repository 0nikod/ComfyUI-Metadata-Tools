# Save Image (Metadata)

This node saves images to the output folder while embedding custom metadata provided as a string or JSON.

## Inputs

- **images**: The images to be saved.
- **metadata_text**: A string or JSON object containing the metadata you want to embed. If it's valid JSON, it will be parsed and added as key-value pairs; otherwise, it will be added as a "UserMetadata" entry.
- **filename_prefix**: The prefix for the saved file.

## Features

- **Automatic Inclusion**: Automatically includes the current workflow and prompt in the PNG metadata if available.
- **Custom Metadata**: Allows adding any custom text or JSON data to the image info.

## Usage

Use this node to save your final results while ensuring that important information (like specific settings or tags) is stored directly inside the image file for future reference.
