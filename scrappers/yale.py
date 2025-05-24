import requests
from bs4 import BeautifulSoup
import time


def get_yale_transcripts(url):
    """
    Get all lecture transcripts from a Yale Open Course.
    
    Args:
        url (str): Course URL (e.g., https://oyc.yale.edu/english/engl-291)
    
    Returns:
        dict: Dictionary with lecture titles as keys and their transcripts as values
    """
    def get_page(url):
        try:
            response = requests.get(url, timeout=10)
            return BeautifulSoup(response.content, 'html.parser') if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_transcript(lecture_url):
        soup = get_page(lecture_url)
        if not soup:
            return None
        
        transcript_div = soup.find('h1', {'id': 'transcript-top'})
        if transcript_div and transcript_div.parent:
            return transcript_div.parent.get_text()
        return None

    lectures = {}
    soup = get_page(url)
    if not soup:
        return lectures

    # Find lectures container and get all links
    lectures_div = soup.select_one('#quicktabs-tabpage-course_quicktabs-2 > div:nth-child(2) > div > div')
    if not lectures_div:
        return lectures

    for link in lectures_div.find_all('a', href=True):
        title = link.get_text(strip=True)
        lecture_url = f"https://oyc.yale.edu{link['href']}"
        
        print(f"Getting transcript for: {title}")
        transcript = get_transcript(lecture_url)
        if transcript:
            lectures[title] = transcript
        

    return lectures


if __name__ == "__main__":
    course_url = "https://oyc.yale.edu/english/engl-291"
    transcripts = get_yale_transcripts(course_url)
    
    print(f"\nFound {len(transcripts)} lectures:")
    for title, transcript in transcripts.items():
        print(f"\nLecture: {title}")
        print(f"Transcript preview: {transcript}...")