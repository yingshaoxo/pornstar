import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv

import io
import tempfile
import os
import hashlib
import datetime

from auto_everything.video import VideoUtils, Video, Disk, Terminal
from auto_everything.disk import Store

terminal = Terminal()
disk = Disk()
video = Video()
videoUtils = VideoUtils()

from . import utils


class AudioClassifier():
    def __init__(self):
        # Load the model.
        filename = "yamnet_1.tar.gz"
        url = f"https://github.com/yingshaoxo/pornstar/raw/master/models/{filename}"
        compressedFile = os.path.join(utils.ROOT_DIR, filename)
        if not utils.disk.exists(compressedFile) or (disk.get_file_size(compressedFile, "MB") < 5):
            terminal.run_command(f"rm {compressedFile}")
            print("downloading...")
            utils.network.download(url, compressedFile)
        localModelFolder = os.path.join(utils.ROOT_DIR, "yamnet")
        modelPath = os.path.join(localModelFolder, "saved_model.pb")
        if not utils.disk.exists(modelPath):
            utils.disk.uncompress(compressedFile, localModelFolder)
        self.model = hub.load(localModelFolder)  # .signatures['default']

        class_map_path = self.model.class_map_path().numpy()
        class_map_csv_text = tf.io.read_file(class_map_path).numpy().decode('utf-8')
        class_map_csv = io.StringIO(class_map_csv_text)
        class_names = [display_name for (class_index, mid, display_name) in csv.reader(class_map_csv)]
        self.class_names = class_names[1:]  # Skip CSV header

        # Input: 3 seconds of silence as mono 16 kHz waveform samples.
        waveform = np.zeros(3 * 16000, dtype=np.float32)
        self.store = Store("AudioClassifier")

    def get_waveform_list_from_video(self, videoPath: str, secondsForOnePart=3):
        self.temp_dir: str = tempfile.gettempdir()
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode("utf-8"))
        m.update(videoPath.encode("utf-8"))
        temp_audio_file = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".wav")
        videoUtils.convert_video_to_wav(videoPath, temp_audio_file)
        soundArray, SampleRate = videoUtils.get_mono_16khz_audio_array(temp_audio_file)
        os.remove(temp_audio_file)
        return videoUtils.convert_array_to_batch_samples(soundArray, secondsForOnePart)

    def classify(self, waveform):
        # https://tfhub.dev/google/yamnet/1
        # Run the model, check the output.
        scores, embeddings, log_mel_spectrogram = self.model(waveform)
        scores.shape.assert_is_compatible_with([None, 521])
        embeddings.shape.assert_is_compatible_with([None, 1024])
        log_mel_spectrogram.shape.assert_is_compatible_with([None, 64])
        result = self.class_names[scores.numpy().mean(axis=0).argmax()]  # Should print 'Silence'.
        # print(result)
        return result

    def label_a_video_with_intervals(self, videoPath: str, intervalLength=3):
        if self.store.get("lastVideo", "") == videoPath:
            intervalsAndLabels = self.store.get("intervalsAndLabels", "[]")
            if intervalsAndLabels != []:
                return intervalsAndLabels[0], intervalsAndLabels[1]
        waveformList = self.get_waveform_list_from_video(videoPath, secondsForOnePart=intervalLength)
        labels = []
        intervals = []
        for i, waveform in enumerate(waveformList):
            a = i * intervalLength
            b = a + intervalLength
            intervals.append([a, b])
            result = self.classify(waveform)
            labels.append(result)
            # print(i, result)
        return intervals, labels
