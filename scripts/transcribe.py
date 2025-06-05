import os
import time
from pathlib import Path
import pandas as pd
import whisperx
from utils import log
from config import RUN_CONFIG, HF_TOKEN

class Transcriber:
    """Transcribes and diarizes audio files using WhisperX."""

    def __init__(self, log_name, token=HF_TOKEN):
        """
        Initialize transcriber.

        Args:
            log_name (str): Name for logging.
            token (str): Hugging Face token for diarization.
        """
        self.config = RUN_CONFIG
        self.transcript_dir = Path("transcripts")
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        self.model = whisperx.load_model(
            self.config.get('model_size'),
            self.config.get('device'),
            compute_type=self.config.get('compute_type')
        )
        self.token = token
        self.logger = log(f'{log_name}_transcribe')

    def transcribe(self, audio_path):
        """
        Transcribe and diarize a given audio file.

        Args:
            audio_path (Path): Path to audio file.

        Returns:
            None
        """
        try:
            output_file = self.transcript_dir / (audio_path.stem + "_trans.json")

            if output_file.exists():
                self.logger.info(f"Skipping {audio_path.name} — transcript already exists.")
                return

            self.logger.info(f"Transcribing {audio_path.name}")
            filesize = round(os.path.getsize(audio_path) / (1024 * 1024), 1)
            self.logger.info(f"File size: {filesize} MB")

            audio = whisperx.load_audio(str(audio_path))
            result = self.model.transcribe(str(audio_path), batch_size=self.config.get("batch_size", 16))

            self.logger.info(f'Diarizing {audio_path.name}')
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=self.token, device=self.config.get('device'))
            diarized_segments = diarize_model(audio)
            diarized = whisperx.assign_word_speakers(diarized_segments, result)

            outdf = pd.DataFrame(diarized['segments'])
            outdf['episode_id'] = audio_path.stem.split('__')[1]
            outdf.rename(columns={
                'text': 'transcript',
                'start': 'start_time',
                'end': 'end_time'
            }, inplace=True)

            arrange_cols = ['episode_id', 'speaker', 'start_time', 'end_time', 'transcript']
            outdf = outdf[arrange_cols]

            outdf.to_json(output_file, orient='records', lines=True)
            self.logger.info(f'Saved transcription to {output_file}')
        except Exception as e:
            self.logger.error(f"Failed to transcribe {audio_path.name}: {e}")
