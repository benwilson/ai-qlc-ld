#!/usr/bin/env python3
import unittest

from qlc_runtime.vlc_http import (
    VlcStatus,
    extract_media_basename,
    parse_vlc_status_payload,
)


class VlcHttpTests(unittest.TestCase):
    def test_parse_status_payload(self):
        status = parse_vlc_status_payload(
            {
                "state": "playing",
                "time": 42,
                "length": 180,
                "information": {
                    "category": {
                        "meta": {
                            "url": "file:///Users/test/Music/Track%20Name.mp3",
                            "filename": "Track Name.mp3",
                            "title": "Track Name",
                        }
                    }
                },
            }
        )
        self.assertEqual(status.state, "playing")
        self.assertEqual(status.time_s, 42.0)
        self.assertEqual(status.length_s, 180.0)
        self.assertEqual(status.media_uri, "file:///Users/test/Music/Track%20Name.mp3")

    def test_extract_media_basename_prefers_uri(self):
        status = VlcStatus(
            state="playing",
            time_s=0.0,
            length_s=None,
            media_uri="file:///Users/test/Music/Another%20Song.flac",
            filename="ignore-me.mp3",
            title="Ignore Me",
        )
        self.assertEqual(extract_media_basename(status), "Another Song.flac")

    def test_extract_media_basename_fallbacks(self):
        no_uri = VlcStatus(
            state="playing",
            time_s=0.0,
            length_s=None,
            media_uri=None,
            filename="FromFilename.wav",
            title="From Title",
        )
        self.assertEqual(extract_media_basename(no_uri), "FromFilename.wav")

        title_only = VlcStatus(
            state="playing",
            time_s=0.0,
            length_s=None,
            media_uri=None,
            filename=None,
            title="From Title",
        )
        self.assertEqual(extract_media_basename(title_only), "From Title")


if __name__ == "__main__":
    unittest.main()
