import os
import time
import feedparser
import requests
from datetime import datetime
from pathlib import Path
import pandas as pd

from utils import log, to_seconds

class DownloadPodcast:
    """Downloads podcast episodes and stores metadata."""

    def __init__(self, download_path, log_name, year=2024):
        """
        Initialize downloader with save paths and logging.

        Args:
            download_path (str): Directory where podcasts will be downloaded.
            log_name (str): Name to use for logging.
            year (int): Only download episodes published in this year.
        """
        self.year = year
        self.download_path = Path(download_path)
        self.download_path.mkdir(parents=True, exist_ok=True)

        self.metadata_path = Path('metadata')
        self.metadata_path.mkdir(parents=True, exist_ok=True)

        self.outname = log_name
        self.metadata = []
        self.podcast = None
        self.logger = log(f'{log_name}_download')

    def save_metadata(self):
        """
        Save metadata of downloaded episodes to CSV.

        Returns:
            Path: Output path of the saved metadata CSV.
        """
        if not self.metadata:
            self.logger.warning("No metadata to save.")
            return None

        try:
            df = pd.DataFrame(self.metadata)
            self.logger.info(f'Podcast {self.podcast} had {len(df)} episodes in {self.year}')
            outpath = self.metadata_path / self.outname
            df.to_csv(f"{outpath}_metadata.csv", index=False)
            self.logger.info(f'Metadata saved to {outpath}_metadata.csv')
            return f"{outpath}_metadata.csv"
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")
            return None

    def download_feed(self, rss_url):
        """
        Parse RSS feed and download audio episodes.

        Args:
            rss_url (str): URL of the podcast RSS feed.

        Returns:
            str: Path to saved metadata CSV.
        """
        try:
            feed = feedparser.parse(rss_url)
            self.podcast = feed.feed.get('title', 'unknown').replace(' ', '_').lower()

            for entry in feed.entries:
                pub_date = datetime(*entry.published_parsed[:6])
                if self.year and pub_date.year != self.year:
                    continue

                audio_url = next((l.href for l in entry.links if 'audio' in l.type), None)
                if not audio_url:
                    continue

                episode_id = os.path.basename(entry.id).split(':')[-1]
                filename = f"{self.podcast}__{episode_id}.mp3"
                filepath = self.download_path / filename

                if filepath.exists():
                    continue

                self.metadata.append({
                    'podcast': self.podcast,
                    'podcast_url': entry.title_detail.base,
                    'title': entry.title,
                    'episode_id': episode_id,
                    'published_on': pd.to_datetime(entry.published),
                    'pub_date': pd.to_datetime(entry.published).date(),
                    'audio_url': audio_url,
                    'duration': to_seconds(entry.itunes_duration),
                    'filename': str(filepath)
                })

                try:
                    r = requests.get(audio_url)
                    r.raise_for_status()
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    self.logger.info(f'Downloaded {filename}')
                    time.sleep(5)
                except Exception as e:
                    self.logger.error(f"Failed to download {filename}: {e}")

            return self.save_metadata()

        except Exception as e:
            self.logger.error(f"Failed to process RSS feed: {e}")
            return None
