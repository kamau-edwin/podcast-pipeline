import os
import time
import click
import pandas as pd
from pathlib import Path

from scripts.download import DownloadPodcast
from scripts.transcriber import Transcriber
from scripts.utils import log

@click.command()
@click.option(
    "-u", "--rss_url", required=True,
    help="RSS feed URL to download podcast episodes from."
)
@click.option(
    "-p", "--download_path", required=True,
    help="Directory path where podcast episodes will be saved."
)
def main(rss_url, download_path):
    """
    Download and transcribe podcast episodes from a given RSS feed.
    
    Args:
        rss_url (str): URL of the podcast RSS feed.
        download_path (str): Path to save downloaded episodes.
    """
    start = time.time()
    log_name = os.path.basename(rss_url).lower().replace('.', '_')
    logger = log(f'main_{log_name}')
    
    try:
        logger.info(f'Starting download and transcription for RSS: {rss_url}')
        
        downloader = DownloadPodcast(download_path, log_name)
        transcriber = Transcriber(log_name)

        metadata_file_path = downloader.download_feed(rss_url)
        
        if not metadata_file_path or not os.path.exists(metadata_file_path):
            logger.error(f"Metadata file not found or empty: {metadata_file_path}")
            return

        episodes = pd.read_csv(metadata_file_path, usecols=['filename'])
        for filepath in episodes['filename']:
            audio_file = Path(filepath)
            if audio_file.exists():
                transcriber.transcribe(audio_file)
            else:
                logger.warning(f"Audio file not found: {filepath}")
        
        logger.info(f"Download and transcription process completed for RSS: {rss_url}")
        logger.info(f"Total time: {(time.time() - start) / 60:.2f} minutes")
    
    except Exception as e:
        logger.error(f"Failed main process for {rss_url}: {e}")

if __name__ == "__main__":
    main()
