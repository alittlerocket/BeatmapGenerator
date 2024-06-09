from parsing.parse import *
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
        e = self.map1.editor
        self.assertEqual(e.Bookmarks, [8766,25608,42450,59292,76134,92976,97187,114029,119292,130871,147713,164555,181397,198239,215081,231923,248765])
        self.assertEqual(e.DistanceSpacing, 0.9)
        self.assertEqual(e.BeatDivisor, 8)
        self.assertEqual(e.GridSize, 32)
        self.assertAlmostEqual(e.TimelineZoom, 3, places=5)

    def test_metadata(self):
        m = self.map1.metadata
        self.assertEqual(m.Title, "Loop (feat. WaMi)")
        self.assertEqual(m.TitleUnicode, "Loop (feat. WaMi)")
        self.assertEqual(m.Artist, "Yunosuke")
        self.assertEqual(m.ArtistUnicode, "雄之助")
        self.assertEqual(m.Creator, "Kotoha")
        self.assertEqual(m.Version, "Rtyzen's Insane")
        self.assertEqual(m.Source, "")
        self.assertEqual(m.Tags, "keywee vebox ayucchi rtyzen mocaotic featured artist fa wami japanese electronic sinsekai studio city project 深脊界 thinkr mappers' guild mpg".split(" "))
        self.assertEqual(m.BeatmapID, 3589480)
        self.assertEqual(m.BeatmapSetID, 1753970)

    def test_difficulty(self):
        d = self.map1.difficulty
        self.assertEqual(d.HPDrainRate, 5)
        self.assertEqual(d.CircleSize, 4)
        self.assertEqual(d.OverallDifficulty, 8)
        self.assertEqual(d.ApproachRate, 9)
        self.assertEqual(d.SliderMultiplier, 2)
        self.assertEqual(d.SliderTickRate, 1)

    def test_events(self):
        ev = self.map1.events

        # Check the number of events parsed
        self.assertEqual(len(ev.events), 3)

        # Check the first event (Background)
        self.assertEqual(ev.events[0], {
            "type": "Background",
            "filename": "EullhpZVkAMXggL.jpg",
            "offset": (0, 0)
        })

        # Check the second event (Break)
        self.assertEqual(ev.events[1], {
            "type": "Break",
            "startTime": 93176,
            "endTime": 96587
        })

        # Check the third event (Break)
        self.assertEqual(ev.events[2], {
            "type": "Break",
            "startTime": 164754,
            "endTime": 171850
        })
    
    def test_timing_points(self):
        tp = self.map1.timingPoints

        for point in tp.timing_points:
            count = 0
            if len(point) != 8:
                count += 1
                self.fail(f"Incorrect number of parts for point {count}")
        
        # 127th point.
        self.assertAlmostEqual(tp.timing_points[126], [66397,-66.6666666666667,4,2,2,70,0,0])

        # 1st point
        self.assertAlmostEqual(tp.timing_points[0], [345,526.315789473684,4,2,1,40,1,0])

    def test_colours(self):
        c = self.map1.colours

        self.assertEqual(c.combo_colors, {
            "Combo1" : (191,173,225),
            "Combo2" : (197,217,106),
            "Combo3" : (97,75,183),
            "Combo4" : (181,203,253)
        })
    
    def test_hit_objects(self):
        ho = self.map1.hitObjects

        slider = ho.hit_objects[8]
        circle = ho.hit_objects[15]

        self.assertIsInstance(slider, Slider)
        self.assertEqual(slider.x, 452)
        self.assertEqual(slider.y, 191)
        self.assertEqual(slider.time, 4555)
        self.assertEqual(slider.type_flags, 2)
        self.assertEqual(slider.curveType, 'B')
        self.assertEqual(slider.slides, 1)
        self.assertEqual(slider.length, 300.0)

        self.assertIsInstance(circle, Circle)
        self.assertEqual(circle.x, 261)
        self.assertEqual(circle.y, 241)
        self.assertEqual(circle.time, 8239)
        self.assertEqual(circle.type_flags, 5)


if __name__ == "__main__":
    unittest.main()
