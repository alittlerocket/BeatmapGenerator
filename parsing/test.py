from parse_beatmap import *
import unittest

class BeatmapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Relative path to the .osu file
        path = "../data/map1.osu"

        # Create beatmap obj with .osu file
        cls.map1 = create_beatmap_from_file(file_path=path)

    def test_general(self):
        g = self.map1.general
        self.assertEqual(g.AudioFilename, "audio.mp3")
        self.assertEqual(g.AudioLeadIn, 0)
        self.assertEqual(g.PreviewTime, 59226)
        self.assertEqual(g.Countdown, 0)
        self.assertEqual(g.SampleSet, "Soft")
        self.assertEqual(g.StackLeniency, 0.4)
        self.assertEqual(g.Mode, 0)
        self.assertEqual(g.LetterboxInBreaks, 0)
        self.assertEqual(g.WidescreenStoryboard, 1)

    def test_editor(self):
        

if __name__ == "__main__":
    unittest.main()
