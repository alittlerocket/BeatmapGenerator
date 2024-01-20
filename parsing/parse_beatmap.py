import numpy as np
from typing import List, Union

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
        self.AudioFilename = None
        self.AudioLeadIn = 0
        self.AudioHash = None  # Deprecated
        self.PreviewTime = -1
        self.Countdown = 1
        self.SampleSet = "Normal"
        self.StackLeniency = 0.7
        self.Mode = 0
        self.LetterboxInBreaks = 0
        self.StoryFireInFront = 1  # Deprecated
        self.UseSkinSprites = 0
        self.AlwaysShowPlayfield = 0  # Deprecated
        self.OverlayPosition = "NoChange"
        self.SkinPreference = None
        self.EpilepsyWarning = 0
        self.CountdownOffset = 0
        self.SpecialStyle = 0
        self.WidescreenStoryboard = 0
        self.SamplesMatchPlaybackRate = 0
    
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
        else:
            return value

class Editor(Section):
    def __init__(self):
        self.Bookmarks = []  # List of integers
        self.DistanceSpacing = 1.0  # Decimal
        self.BeatDivisor = 4  # Integer
        self.GridSize = 4  # Integer
        self.TimelineZoom = 1.0  # Decimal

    def _cast_value(self, key: str, value: str) -> Union[List[int], float, int]:
        if key == 'Bookmarks':
            return [int(x) for x in value.split(',')]
        elif key in ['DistanceSpacing', 'TimelineZoom']:
            return float(value)
        elif key in ['BeatDivisor', 'GridSize']:
            return int(value)
        else:
            return value

class Metadata(Section):
    def __init__(self):
        self.Title = ""
        self.TitleUnicode = ""
        self.Artist = ""
        self.ArtistUnicode = ""
        self.Creator = ""
        self.Version = ""
        self.Source = ""
        self.Tags = []  # List of strings
        self.BeatmapID = 0
        self.BeatmapSetID = 0

    def _cast_value(self, key: str, value: str):
        if key in ['BeatmapID', 'BeatmapSetID']:
            return int(value)
        elif key == 'Tags':
            return value.split()  # Splitting by spaces
        else:
            return value

class Difficulty(Section):
    def __init__(self):
        self.HPDrainRate = 5.0  
        self.CircleSize = 5.0  
        self.OverallDifficulty = 5.0  
        self.ApproachRate = 5.0  
        self.SliderMultiplier = 1.0  
        self.SliderTickRate = 1.0  

class Events(Section):
    def __init__(self):
        self.events = []

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
        self.combo_colors = {}  # Stores combo colors in a dictionary
        self.slider_track_override = None
        self.slider_border = None

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

    def to_dict(self) -> dict:
        return {
            "combo_colors": self.combo_colors,
            "slider_track_override": self.slider_track_override,
            "slider_border": self.slider_border
        }

### DATA ###
class TimingPoints:
    def __init__(self):
        self.timing_points = []

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

    def to_numpy(self) -> np.ndarray:
        return np.array(self.timing_points)

    def to_list(self) -> list:
        return self.timing_points

class HitObjects:
    def __init__(self):
        self.hit_objects = []

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line:
                hit_object = HitObject.create(line)
                self.hit_objects.append(hit_object)

class HitObject:
    def __init__(self, x, y, time, type_flags, hit_sound, hit_sample):
        self.x = int(x)
        self.y = int(y)
        self.time = int(time)
        self.type_flags = int(type_flags)
        self.hit_sound = int(hit_sound)
        self.hit_sample = hit_sample.split(':')
        self.new_combo = self.type_flags & 4 > 0
        self.combo_skip = (self.type_flags >> 4) & 7

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
    def __init__(self, x, y, time, type_flags, hit_sound, object_params, hit_sample):
        super().__init__(x, y, time, type_flags, hit_sound, hit_sample)

        # Basic Slider Params
        curve = object_params[0].split('|')
        self.curveType = curve[0]
        self.curvePoints = [self._parse_point(point) for point in curve[1:]]
        self.slides = object_params[1]
        self.length = object_params[2]
        
        # Edgesounds
        if len(object_params) > 3:
            self.edgeSounds = [int(sound) for sound in object_params[3].split('|')]
        else:
            self.edgeSounds = []

        # Edgesets
        if len(object_params) > 4:
            self.edgeSets = object_params[4].split('|')
        else:
            self.edgeSets = []
    
    def _parse_point(self, point_str):
        x, y = point_str.split(':')
        return int(x), int(y)
        
class Spinner(HitObject):
    def __init__(self, x, y, time, type_flags, hit_sound, object_params, hit_sample):
        super().__init__(x, y, time, type_flags, hit_sound, hit_sample)
        self.end_time = int(object_params[0])

### BEATMAP OBJECT
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
        
        self.general = general
        self.editor = editor
        self.metadata = metadata
        self.difficulty = difficulty
        self.events = events
        self.timingPoints = timingPoints
        self.colours = colours
        self.hitObjects = hitObjects

### Wrapper function ###
def create_beatmap_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sections = {"[General]": "", "[Editor]": "", "[Metadata]": "", "[Difficulty]": "",
                "[Events]": "", "[TimingPoints]": "", "[Colours]": "", "[HitObjects]": ""}
    current_section = None

    for line in lines:
        line = line.strip()
        if line in sections:
            current_section = line
            continue

        if current_section and line:
            sections[current_section] += line + '\n'

    general = General(sections["[General]"])
    editor = Editor(sections["[Editor]"])
    metadata = Metadata(sections["[Metadata]"])
    difficulty = Difficulty(sections["[Difficulty]"])
    events = Events(sections["[Events]"])
    timing_points = TimingPoints(sections["[TimingPoints]"])
    colours = Colours(sections["[Colours]"])
    hit_objects = HitObjects(sections["[HitObjects]"])

    return Beatmap(general, editor, metadata, difficulty, events, timing_points, colours, hit_objects)