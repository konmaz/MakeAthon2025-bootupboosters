import io

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class LectureTranscript:
    title: str
    transcript: Optional[str]


def get_yale_transcripts(url: str) -> List[LectureTranscript]:
    """
    Get all lecture transcripts from a Yale Open Course.

    Args:
        url (str): Course URL (e.g., https://oyc.yale.edu/english/engl-291)

    Returns:
        List[LectureTranscript]: List of transcript entries
    """
    def get_page(url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, timeout=10)
            return BeautifulSoup(response.content, 'html.parser') if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_transcript(lecture_url: str) -> Optional[str]:
        soup = get_page(lecture_url)
        if not soup:
            return None

        transcript_div = soup.find('h1', {'id': 'transcript-top'})
        if transcript_div and transcript_div.parent:
            return transcript_div.parent.get_text()
        return None

    soup = get_page(url)
    if not soup:
        return []

    # Select the lecture links container
    lectures_div = soup.select_one('#quicktabs-tabpage-course_quicktabs-2 > div:nth-child(2) > div > div')
    if not lectures_div:
        return []

    lectures: List[LectureTranscript] = []

    for link in lectures_div.find_all('a', href=True)[0:2]:
        title = link.get_text(strip=True)
        lecture_url = f"https://oyc.yale.edu{link['href']}"

        print(f"Getting transcript for: {title}")
        transcript = get_transcript(lecture_url)

        lectures.append(LectureTranscript(title=title, transcript=transcript))

    return lectures

def serialize_transcripts_to_bytesio(lectures: List[LectureTranscript]) -> io.BytesIO:
    buffer = io.BytesIO()
    text = ""

    for i, lecture in enumerate(lectures, start=1):
        text += f"Lecture {i}: {lecture.title}\n"
        text += "\n--- Transcript ---\n"
        text += (lecture.transcript or "Transcript not available").strip()
        text += "\n\n" + "=" * 80 + "\n\n"

    buffer.write(text.encode("utf-8"))
    buffer.seek(0)  # reset cursor to start for reading
    return buffer

if __name__ == "__main__":
    course_url = "https://oyc.yale.edu/english/engl-291"
    transcripts = get_yale_transcripts(course_url)

    print(f"\nFound {len(transcripts)} lectures:")
    for entry in transcripts:
        print(f"\nLecture: {entry.title}")
        print(f"Transcript preview: {entry.transcript[:300] if entry.transcript else 'No transcript'}...")
