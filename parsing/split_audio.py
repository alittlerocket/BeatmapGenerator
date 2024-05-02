from spleeter.separator import Separator


def spleet(
    filename: str,
    dest: str,
    num_stems: int = 2
):
    """
        Split the audio file and outputs to a given directory.

        Parameters:
        - filename: str - The path to the source audio file.
        - dest: str - The directory where the separated audio files will be saved.
        - stems: str - The spleeter configuration for the number of stems (default is 'spleeter:2stems').

        Raises:
        - Exception: If there is any error in loading, separating, or saving the audio.
    """

    try:
        separator = Separator(f'spleeter:{num_stems}stems')
        separator.separate_to_file(audio_descriptor=filename, destination=dest)
        print("Separation OK")
    except Exception as e:
        print(f"Cannot separate audio: {e}")



