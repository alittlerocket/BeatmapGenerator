import numpy as np
from typing import List, Dict, Tuple, Union, Optional

### SECTIONS ###
class Section:
    def load_from_string(self, 
                         data_string
        ) -> None:
        """
        Given the appropriate data string, parse it and set the
        corresponding attributes
        """

        for line in data_string.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Assign value to the corresponding attribute
                if hasattr(self, key):
                    setattr(self, key, self._cast_value(key, value))

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the General section
        """

        return {attr: getattr(self, attr) for attr in self.__dict__}

class General(Section):
    def __init__(self):
        self.AudioFilename: Optional[str] = None
        self.AudioLeadIn: int = 0
        self.AudioHash: Optional[str] = None  # Deprecated
        self.PreviewTime: int = -1
        self.Countdown: int = 1
        self.SampleSet: str = "Normal"
        self.StackLeniency: float = 0.7
        self.Mode: int = 0
        self.LetterboxInBreaks: int = 0
        self.StoryFireInFront: int = 1  # Deprecated
        self.UseSkinSprites: int = 0
        self.AlwaysShowPlayfield: int = 0  # Deprecated
        self.OverlayPosition: str = "NoChange"
        self.SkinPreference: Optional[str] = None
        self.EpilepsyWarning: int = 0
        self.CountdownOffset: int = 0
        self.SpecialStyle: int = 0
        self.WidescreenStoryboard: int = 0
        self.SamplesMatchPlaybackRate: int = 0
    
    def _cast_value(self, 
                    key, 
                    value
        ) -> Union[int, float, str]:
        """
        Convert value to the appropriate type
        """

        if key in ['AudioLeadIn', 'PreviewTime', 'Countdown', 'Mode', 'LetterboxInBreaks', 
                   'StoryFireInFront', 'UseSkinSprites', 'AlwaysShowPlayfield', 'EpilepsyWarning', 
                   'CountdownOffset', 'SpecialStyle', 'WidescreenStoryboard', 'SamplesMatchPlaybackRate']:
            return int(value)
        elif key in ['StackLeniency']:
            return float(value)
        elif key in ['AudioFilename', 'AudioHash', 'SampleSet', 'OverlayPosition', 'SkinPreference']:
            return value
        else:
            raise Exception("General: Key not found")

class Editor(Section):
    def __init__(self):
        self.Bookmarks: List[int] = []  # List of integers
        self.DistanceSpacing: float = 1.0  # Decimal
        self.BeatDivisor: int = 4  # Integer
        self.GridSize: int = 4  # Integer
        self.TimelineZoom: float = 1.0  # Decimal


    def _cast_value(self, key: str, value: str) -> Union[List[int], float, int]:
        if key == 'Bookmarks':
            return [int(x) for x in value.split(',')]
        elif key in ['DistanceSpacing', 'TimelineZoom']:
            return float(value)
        elif key in ['BeatDivisor', 'GridSize']:
            return int(value)
        else:
            raise Exception("Editor: Key not found")

class Metadata(Section):
    def __init__(self):
        self.Title: str = ""
        self.TitleUnicode: str = ""
        self.Artist: str = ""
        self.ArtistUnicode: str = ""
        self.Creator: str = ""
        self.Version: str = ""
        self.Source: str = ""
        self.Tags: List[str] = []
        self.BeatmapID: int = 0
        self.BeatmapSetID: int = 0

    def _cast_value(self, key: str, value: str):
        if key in ['BeatmapID', 'BeatmapSetID']:
            return int(value)
        elif key == 'Tags':
            return value.split()  # Splitting by spaces
        elif key in ['Title', 'TitleUnicode', 'Artist',
                     'ArtistUnicode', 'Creator', 'Version', 'Source']:
            return value
        else:
            raise Exception("Metadata: Key not found")

class Difficulty(Section):
    def __init__(self):
        self.HPDrainRate: float = 5.0  
        self.CircleSize: float = 5.0  
        self.OverallDifficulty: float = 5.0  
        self.ApproachRate: float = 5.0  
        self.SliderMultiplier: float = 1.0  
        self.SliderTickRate: float = 1.0  
    
    def _cast_value(self, key: str, value: str):
        if key in ['HPDrainRate', 'CircleSize', 'OverallDifficulty',
                   'ApproachRate', 'SliderMultiplier', 'SliderTickRate']:
            return float(value)
        else:
            raise Exception("Difficulty: Key not found")

class Events(Section):
    def __init__(self):
        self.events: List[Dict] = []

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('//'):  # Ignore empty lines and comments
                self.events.append(self._parse_event_line(line))

    def _parse_event_line(self, line: str):
        parts = line.split(',')
        event_type = parts[0].strip()

        if event_type in ["0", "Background"] and len(parts) >= 3:
            return {
                "type": "Background",
                "filename": parts[2].strip(' "'),  # Removing potential quotes
                "offset": (int(parts[3]), int(parts[4])) if len(parts) >= 5 else (0, 0)
            }
        elif event_type in ["Video", "1"] and len(parts) >= 3:
            return {
                "type": "Video",
                "startTime": int(parts[1]),
                "filename": parts[2].strip(' "'),
                "offset": (int(parts[3]), int(parts[4])) if len(parts) >= 5 else (0, 0)
            }
        elif event_type in ["2", "Break"] and len(parts) == 3:
            return {
                "type": "Break",
                "startTime": int(parts[1]),
                "endTime": int(parts[2])
            }
        else:
            return {"type": "Unknown", "data": line}

    def to_dict(self) -> dict:
        return {"events": self.events}

class Colours(Section):
    def __init__(self):
        self.combo_colors: Dict = {}
        self.slider_track_override: Optional[Tuple] = None
        self.slider_border: Optional[Tuple] = None

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = tuple(map(int, parts[1].strip().split(',')))

                    if key.startswith('Combo'):
                        self.combo_colors[key] = value
                    elif key == 'SliderTrackOverride':
                        self.slider_track_override = value
                    elif key == 'SliderBorder':
                        self.slider_border = value
                    else:
                        raise Exception("Colours: Key not found")

    def to_dict(self) -> dict:
        return {
            "combo_colors": self.combo_colors,
            "slider_track_override": self.slider_track_override,
            "slider_border": self.slider_border
        }

### DATA ###
class TimingPoints:
    def __init__(self):
        self.timing_points: List[List[Union[int, float]]] = []

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 8:
                    self.timing_points.append([
                        int(parts[0]),     # time
                        float(parts[1]),  # beat_length
                        int(parts[2]),    # meter
                        int(parts[3]),    # sample_set
                        int(parts[4]),    # sample_index
                        int(parts[5]),    # volume
                        bool(int(parts[6])),  # uninherited
                        int(parts[7])     # effects
                    ])
                else:
                    raise Exception(f"TimingPoints: Incorrect number of arguments (Need 8, got {len(parts)})")

    def to_numpy(self) -> np.ndarray:
        return np.array(self.timing_points)

class HitObjects:
    def __init__(self):
        self.hit_objects: List[HitObject] = []

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line:
                hit_object = HitObject.create(line)
                self.hit_objects.append(hit_object)

class HitObject:
    def __init__(self, x, y, time, type_flags, hit_sound, hit_sample):
        self.x: int = x
        self.y: int = y
        self.time: int = time
        self.type_flags: int = type_flags
        self.hit_sound: int = hit_sound
        self.hit_sample: List[str] = hit_sample.split(':')
        self.new_combo: bool = self.type_flags & 4 > 0
        self.combo_skip: int = (self.type_flags >> 4) & 7

    @staticmethod
    def create(line):
        parts = line.split(',')
        x, y, time, type_flags, hit_sound, *object_params, hit_sample = parts
        hit_object_type = int(type_flags)

        if hit_object_type & 1:
            return Circle(x, y, time, type_flags, hit_sound, hit_sample)
        elif hit_object_type & 2:
            return Slider(x, y, time, type_flags, hit_sound, object_params, hit_sample)
        elif hit_object_type & 8:
            return Spinner(x, y, time, type_flags, hit_sound, object_params, hit_sample)
        else:
            return HitObject(x, y, time, type_flags, hit_sound, hit_sample)

class Circle(HitObject):
    def __init__(self, x, y, time, type_flags, hit_sound, hit_sample):
        super().__init__(x, y, time, type_flags, hit_sound, hit_sample)

class Slider(HitObject):
    def __init__(self, x: int, y: int, time: int, type_flags: int, hit_sound: int, object_params: List[str], hit_sample: str):
            super().__init__(x, y, time, type_flags, hit_sound, hit_sample)
            curve = object_params[0].split('|')
            self.curveType: str = curve[0]
            self.curvePoints: List[Tuple[int, int]] = [self._parse_point(point) for point in curve[1:]]
            self.slides: int = int(object_params[1])
            self.length: float = float(object_params[2])
            self.edgeSounds: List[int] = [int(sound) for sound in object_params[3].split('|')] if len(object_params) > 3 else []
            self.edgeSets: List[str] = object_params[4].split('|') if len(object_params) > 4 else []
    
    def _parse_point(self, point_str):
        x, y = point_str.split(':')
        return int(x), int(y)
        
class Spinner(HitObject):
    def __init__(self, x, y, time, type_flags, hit_sound, object_params, hit_sample):
        super().__init__(x, y, time, type_flags, hit_sound, hit_sample)
        self.end_time: int = int(object_params[0])

### BEATMAP OBJECT ###
class Beatmap:
    def __init__(self, 
                 general: General,
                 editor: Editor,
                 metadata: Metadata,
                 difficulty: Difficulty,
                 events: Events, 
                 timingPoints: TimingPoints, 
                 colours: Colours,
                 hitObjects: HitObjects):
        
        self.general: General = general
        self.editor: Editor = editor
        self.metadata: Metadata = metadata
        self.difficulty: Difficulty = difficulty
        self.events: Events = events
        self.timingPoints: TimingPoints = timingPoints
        self.colours: Colours = colours
        self.hitObjects: HitObjects = hitObjects

### Wrapper function ###
def create_beatmap_from_file(file_path):
    section_classes = {
        "[General]": General,
        "[Editor]": Editor,
        "[Metadata]": Metadata,
        "[Difficulty]": Difficulty,
        "[Events]": Events,
        "[TimingPoints]": TimingPoints,
        "[Colours]": Colours,
        "[HitObjects]": HitObjects
    }
    
    # Initialize sections
    sections = {section: "" for section in section_classes}
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line in section_classes:
                current_section = line
            elif current_section and line:
                sections[current_section] += line + '\n'

    # Create section objects
    section_objects = {name: cls() for name, cls in section_classes.items()}
    for name, data in sections.items():
        section_objects[name].load_from_string(data)

    # Create and return the Beatmap object
    return Beatmap(*section_objects.values())