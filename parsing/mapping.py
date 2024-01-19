import numpy as np

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
        self.object_params = object_params


class Spinner(HitObject):
    def __init__(self, x, y, time, type_flags, hit_sound, object_params, hit_sample):
        super().__init__(x, y, time, type_flags, hit_sound, hit_sample)
        self.end_time = int(object_params[0])


class HitObjects:
    def __init__(self):
        self.hit_objects = []

    def load_from_string(self, data_string: str):
        for line in data_string.strip().split('\n'):
            line = line.strip()
            if line:
                hit_object = HitObject.create(line)
                self.hit_objects.append(hit_object)
