from parsing.parse_beatmap import create_beatmap_from_file

if __name__ == "__main__":
    # Relative path
    path = "data/map1.osu"

    # Create beatmap obj with .osu file
    map1 = create_beatmap_from_file(file_path=path)