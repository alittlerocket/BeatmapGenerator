import librosa, os, numpy as np
from spleeter.separator import Separator
from numpy import ndarray

SAMPLING_RATE = 44100

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
    - num_stems: int - The number of stems to separate the audio into (default is 2).

    Raises:
    - Exception: If there is any error in loading, separating, or saving the audio.
    """

    try:
        separator = Separator(f'spleeter:{num_stems}stems')
        separator.separate_to_file(audio_descriptor=filename, destination=dest)
        print("Separation OK")
    except Exception as e:
        print(f"Cannot separate audio: {e}")

def compute_tempo(
    filepath: str
):
    """
    Compute the tempo and beat times of the given audio file.

    Parameters:
    - filepath: str - The path to the audio file.

    Returns:
    - tempo: ndarray - The estimated tempo of the audio in BPM.
    - beat_times: ndarray - The time values (in seconds) corresponding to the detected beats.
    """
    y, sr = librosa.load(path=filepath)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    beat_times = librosa.frames_to_time(beats, sr=sr)
    return tempo, beat_times

def compute_onsets(
    instrument_dir: str
):
    """
    Compute the onset times for each separated track in the given directory.

    Parameters:
    - instrument_dir: str - The directory containing the separated audio files.

    Returns:
    - all_onset_times: ndarray - Sorted array of all onset times from all tracks.
    """

    # List all files in the output directory
    separated_files = os.listdir(instrument_dir)

    # Extract instrument names and paths.
    separated_tracks = {os.path.splitext(file)[0]: os.path.join(instrument_dir, file) for file in separated_files if file.endswith('.wav')}

    # Loading time series info
    track_data = {}
    for instrument, filepath in separated_tracks.items():
        y, _ = librosa.load(filepath)
        track_data[instrument] = y
    
    # Calculate onset times
    onset_times_by_track = {}
    for instrument, y in track_data.items():
        onset_env = librosa.onset.onset_strength(y=y, sr=SAMPLING_RATE)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env)
        onset_times_by_track[instrument] = librosa.frames_to_time(frames=onset_frames, sr=SAMPLING_RATE)

    all_onset_times = np.hstack(list(onset_times_by_track.values()))
    all_onset_times.sort()

    return all_onset_times

def measure_prioritization(
    tempo: ndarray,
    beat_times: ndarray,
    all_onset_times: ndarray
):
    """
    Prioritize onset times within each measure based on the detected BPM.

    Parameters:
    - tempo: ndarray - The estimated tempo of the audio in BPM.
    - beat_times: ndarray - The time values (in seconds) corresponding to the detected beats.
    - all_onset_times: ndarray - Sorted array of all onset times from all tracks.

    Returns:
    - prioritized_onsets: list - List of prioritized onset times.
    """
    prioritized_onsets = []
    current_bpm = tempo[0]
    measure_duration = 4 * (60 / current_bpm)
    segment_start_time = 0

    for beat_time in beat_times:
        if segment_start_time == 0 or beat_time - segment_start_time > measure_duration:
            segment_end_time = beat_time
            segment_onsets = [time for time in all_onset_times if segment_start_time <= time < segment_end_time]
            if segment_onsets:
                prioritized_onsets.append(segment_onsets[0])
            segment_start_time = segment_end_time
            current_bpm = tempo[0]
            measure_duration = 4 * (60 / current_bpm)

    # Process remaining onsets after the last tempo change
    segment_onsets = [time for time in all_onset_times if segment_start_time <= time]
    if segment_onsets:
        prioritized_onsets.append(segment_onsets[0])

    return prioritized_onsets

def audio_processing(path_to_mp4, instrument_dir, stems=4):
    """
    Process the audio file by separating it into individual instruments, computing the tempo, detecting onsets,
    and prioritizing onsets within each measure.

    Parameters:
    - path_to_mp4: str - The path to the source audio file.
    - instrument_dir: str - The directory where the separated audio files will be saved.
    - stems: int - The number of stems to separate the audio into (default is 4).

    Returns:
    - prioritized_onsets: list - List of prioritized onset times.
    """
    # First split the audio into individual instruments.
    spleet(
        filename=path_to_mp4,
        dest=instrument_dir,
        num_stems=stems
    )

    # Get BPM, beats, and BPM changes
    tempo, beat_times = compute_tempo(filepath=path_to_mp4)

    # Get onset times
    all_onset_times = compute_onsets(instrument_dir=instrument_dir)

    # Get Prioritized Onsets
    prioritized_onsets = measure_prioritization(
        tempo=tempo, beat_times=beat_times, all_onset_times=all_onset_times)
    
    return prioritized_onsets


# # Example usage
# path_to_mp4 = 'path/to/song.mp3'
# instrument_dir = 'output'
# prioritized_onsets = audio_processing(path_to_mp4, instrument_dir)
# create_beatmap(prioritized_onsets)
