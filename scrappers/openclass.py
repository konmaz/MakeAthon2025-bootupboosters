import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def get_course_files(url):
    """
    Get all file URLs from a given OpenCourses URL.
    
    Args:
        url (str): The course URL (e.g., https://opencourses.uoa.gr/modules/document/?course=THEOL2)
    
    Returns:
        set: A set of file URLs found in the course
    """
    def get_page_content(page_url):
        try:
            response = requests.get(page_url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            return None
        except:
            return None

    def extract_course_param(course_url):
        parsed = urlparse(course_url)
        query_params = dict(param.split('=') for param in parsed.query.split('&'))
        return query_params.get('course')

    def get_links(soup, base_url, course_param):
        files = set()
        folders = set()
        if not soup:
            return files, folders

        content_div = soup.find('div', class_='table-responsive')
        if not content_div:
            return files, folders

        visible_rows = content_div.find_all('tr', class_='visible')
        for row in visible_rows:
            for link in row.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                if 'download' in href and f'course={course_param}' in href and (href.endswith('.pdf') or href.endswith(".PDF")):
                    files.add(full_url)
                elif 'openDir' in href and f'course={course_param}' in href:
                    folders.add(full_url)
        return files, folders

    def explore_folder(folder_url, visited):
        if folder_url in visited:
            return set()
        
        visited.add(folder_url)
        parsed_url = urlparse(folder_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        course_param = extract_course_param(folder_url)
        
        soup = get_page_content(folder_url)
        all_files = set()
        
        if soup:
            files, folders = get_links(soup, base_url, course_param)
            all_files.update(files)
            
            for new_folder in folders:
                all_files.update(explore_folder(new_folder, visited))

        return all_files

    return explore_folder(url, set())


if __name__ == "__main__":
    url = input("Enter the course URL: ")
    files = get_course_files(url)
    print("\nFound files:")
    for file in sorted(files):
        print(file)