# Parsing Library

The format of an ".osu" file is pretty much fully detailed in this link:
https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29#metadata

This Beatmap Parser is designed to parse `.osu` files, used in the osu! rhythm game. The parser reads the file and constructs a `Beatmap` object, which contains structured data from various sections of the `.osu` file, such as General, Editor, Metadata, Difficulty, Events, TimingPoints, Colours, and HitObjects.

## Features

- Parses `.osu` beatmap files into structured data.
- Supports all main sections of a beatmap file.
- Converts complex data into Python objects for easy access and manipulation.
- Provides functionality to access individual elements like timing points, hit objects, and more.

## Installation

- No additional installation is required, except for Python and its standard libraries.
- Uses Numpy

```bash
pip install numpy
```

## Structure

The parser consists of several classes representing different sections of the `.osu` file:

* General
* Editor
* Metadata
* Difficulty
* Events
* TimingPoints
* Colours
* HitObjects

Each class is responsible for parsing and storing data from its respective section.

## Usage

1. Ensure `.osu` file is correctly formatted and accessible. It's ok if deprecated items exist in your file.
2. Use the `create_beatmap_from_file` function to parse the file.
```Python
beatmap = create_beatmap_from_file("path/to/your/osu_file.osu")
```
3. Access parsed data via `Beatmap`:

```Python
print(beatmap.general.AudioFilename)
print(beatmap.difficulty.CircleSize)
```

Only exception to this rule is TimingPoints, as it is formatted into a list for data analysis:

```Python
    int(parts[0]),     # time
    float(parts[1]),  # beat_length
    int(parts[2]),    # meter
    int(parts[3]),    # sample_set
    int(parts[4]),    # sample_index
    int(parts[5]),    # volume
    bool(int(parts[6])),  # uninherited
    int(parts[7])     # effects
```

## Customization

You can extend the functionality of the parser by modifying the existing classes or adding new functionality to handle more specific aspects of .osu files.

## License

TBA


