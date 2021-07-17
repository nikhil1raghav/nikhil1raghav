import feedparser
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()
def replace_chunk(content, marker, chunk):
    r=re.compile(r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker,marker),re.DOTALL,)
    chunk="<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker,chunk,marker)
    return r.sub(chunk,content)


def fetch_blog():
    entries = feedparser.parse("https://nikhilraghav.codes/index.xml")["entries"]
    return [
            {
                "title": entry["title"],
                "url": entry["link"].split("#")[0],
            }
            for entry in entries
        ]
    

if __name__ == "__main__":
    readme=root/"README.md"
    entries = fetch_blog()[:8]
    readme_contents=readme.open().read()
    entries_md="\n".join(
            ["* [{title}]({url})".format(**entry) for entry in entries]
            )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)


