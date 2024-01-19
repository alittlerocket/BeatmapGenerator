
from typing import List, Union

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