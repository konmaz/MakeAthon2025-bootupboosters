from scrappers.openclass import get_course_files

# Example usage
url = "https://opencourses.uoa.gr/modules/document/?course=ENL5"
files = get_course_files(url)

# Do something with the files
for file in files:
    print(file)  # or download them, etc.