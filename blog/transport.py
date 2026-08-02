from blog.models import Post, Page
import json
import shutil
from pathlib import Path
from django.conf import settings

def dumpit(self, slug=None, type=None):

    # Validation
    if not slug:
        self.stdout.write(
            "No slug"
        )
    print("DUMP IT")
    if slug:
        print(f"SLUG:{slug}")
    else:
        print("ALL")


    if type == 'page':
        print("PAGE SPECIFIED")
        dump_page = Page.objects.get(slug=slug)
        print(f"DUMPING:{dump_page}")
        page_data = {
                        "title": dump_page.title,
                        "slug": dump_page.slug,
                        # "author": dump_page.author,
                        "content": dump_page.content,
                        # "excerpt": dump_page.excerpt,
                        "status": dump_page.status,
                        # "allow_comments": post.allow_comments,
                        "image": dump_page.image.name if dump_page.image else None,
                        "image_title": dump_page.image_title,
                        "image_alt_text": dump_page.image_alt_text,
                        "created": dump_page.created.isoformat(),
                        "updated": dump_page.updated.isoformat(),
                    }
        # ---------------------------------------------------------
        # WRITE JSON
        # ---------------------------------------------------------
        directory = Path("transport/pages")
        directory.mkdir(parents=True, exist_ok=True) 
        with (directory / f"{slug}.json").open("w", encoding="utf-8") as f:
            json.dump(page_data, f, indent=2)     
        
    elif type == "post":
        print("POST SPECIFIED")
    else:
        print("NO TYPE PASSED")

def loadit(self, slug=None, type=None):
    directory = Path("transport/pages")
    data = ''
    print(f"DIRECTORY: {directory}")
    print(f"SLUG:{slug}")
    with (directory / f"{slug}.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
        print(data)

    obj, created = Page.objects.update_or_create(
    slug=slug,
    defaults={
        "title": data['title'],
        "content": data['content'],
    },
)