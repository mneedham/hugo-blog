import re
import os
import fileinput

pattern = "http://www.markhneedham.com/blog/wp-content/uploads"
replace = "{{<siteurl>}}/uploads"

for root, dirs, files in os.walk("blog/content"):
    for file in files:
        if file.endswith(".md"):
            full_file = os.path.join(root, file)

            with fileinput.FileInput(full_file, inplace=True, backup='.bak') as f:
                for line in f:
                    print(line.replace(pattern, replace), end='')
