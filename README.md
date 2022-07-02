# PNGreencode
A simple project that reencodes PNG files to save storage.
This project was made for my own personal use so it may be missing some features you'd expect. Add your own!

## Warning
Be cautious when using this tool on PNGs with important metadata such as Location tags and HDR as the metadata used will be stripped out!

## Usage
`python pngrecompress.py path [flags]`  
Requires the `pypng` library `pip install png`
- `-r` Process files in subdirectories
- `-w!` Overwrite image files when a more optimal version is generated
- `-o` Specify an output directory to place optimal files into. If relative, based on the current working directory
- `--no-skip` If specified, the new file will be written even if it **doesn't** save space
