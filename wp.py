import MySQLdb
import types
import os
import re

from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse

db=MySQLdb.connect(db="markhneedhamcom_246942_db1", user="root")

c=db.cursor()

c.execute("""\
SELECT p.post_title, p.post_content, p.post_date, p.post_name, p.ID
FROM wp_posts p
WHERE p.post_status = \"publish\"
ORDER BY p.ID DESC""")

for row in c.fetchall():
    content = row[1]

    date = row[2]
    month = '%02d' % date.month
    year = date.year
    day = '%02d' % date.day

    new_content = ""
    for line in content.split("\n"):
        if "<pre" in line:
            if "lang" in line:
                m = re.search("(<pre lang=[\"']?([A-Za-z0-9]+)[\"'].*>?)", line)
                lang = m.group(2)
                line = line.replace(m.group(1), "\n~~~{0}\n".format(lang))
            else:
                line = line.replace("</pre>", "~~~")

        if "</pre>" in line:
            line = line.replace("</pre>", "~~~")
        new_content += line + "\n"
        # print(line)

    # content = soup.prettify()
    content = new_content
    content = content.replace("</p>", "</p>\r\n")
    content = content.replace("&gt;", ">")
    content = content.replace("&lt;", "<")
    content = content.replace("&amp;", "&")

    # content = content.replace("http://www.markhneedham.com/blog/wp-content/uploads", "https://s3-eu-west-1.amazonaws.com/dev.assets.markhneedham.com")

    # print(soup)

    directory = "blog/content/{0}/{1}/{2}".format(year, month, day)
    if not os.path.exists(directory):
        os.makedirs(directory)

    title = row[0].replace("\\", "\\\\").replace('"', r'\"')
    title = title.replace("\2", "\\2")

    print(row[4])

    inner_c=db.cursor()
    inner_c.execute("""\
    select name, slug, taxonomy
    from wp_term_relationships tr
    join wp_term_taxonomy tt ON tt.term_taxonomy_id = tr.term_taxonomy_id
    join wp_terms t ON t.term_id = tt.term_id
    where tr.object_id =  {0}
    """.format(row[4]))

    tags = []
    categories = []
    for irow in inner_c.fetchall():
        if irow[2] == "category":
            categories.append(irow[0])
        if irow[2] == "post_tag":
            tags.append(irow[1])

    f = open("blog/content/{0}/{1}/{2}/{3}.md".format(year, month, day, row[3]), 'w')
    f.write("+++\n")
    f.write("draft = false\n")
    f.write("date=\"{0}\"\n".format(row[2]))
    f.write("title=\"{0}\"\n".format(title))
    f.write("tag={0}\n".format(tags))
    f.write("category={0}\n".format(categories))
    f.write("+++\n\n")
    f.write(content)  # python will convert \n to os.linesep
    f.close()
