from blog.models import Post, Page
import json
from django.contrib.auth.models import User
from pathlib import Path
from django.conf import settings

def dumpit(self, slug=None, type=None, all=None):
    print("DUMPINGIT")
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

    page_data = {}

    if type == 'page':
        print("PAGE SPECIFIED")
        dump_page = []
        if slug is not None:
            dump_page = Page.objects.filter(slug=slug)
        else:
            dump_page = Page.objects.all()
            for d in dump_page:
                print(f"DUMPALL:{d}")
        directory = Path("transport/pages")
        for d in dump_page:
            print(f"DUMPING:{d.slug}")
            page_data = {
                            "title": d.title,
                            "slug": d.slug,
                            # "author": d.author,
                            "content": d.content,
                            "status": d.status,
                            # "allow_comments": post.allow_comments,
                            "image": d.image.name if d.image else None,
                            "image_title": d.image_title,
                            "image_alt_text": d.image_alt_text,
                            "created": d.created.isoformat(),
                            "updated": d.updated.isoformat(),
                        }
            # WRITE JSON
            directory.mkdir(parents=True, exist_ok=True) 
            with (directory / f"{d.slug}.json").open("w", encoding="utf-8") as f:
                json.dump(page_data, f, indent=2)     
    elif type == "post":
        print("POST START")

        dump_post = []
        if slug is not None:
            dump_post = Post.objects.filter(slug=slug)
        else:
            dump_post = Post.objects.all()
        directory = Path("transport/posts")
        for d in dump_post:
            print(f"DUMPING:{d.slug}AUTHOR: {d.author.username}")
            post_data = {
                            "title": d.title,
                            "slug": d.slug,
                             "author": d.author.username,
                            "content": d.content,
                            "excerpt": d.excerpt,
                            "status": d.status,
                             "allow_comments": d.allow_comments,
                            "created": d.created.isoformat(),
                            "updated": d.updated.isoformat(),
                            "published_date":
                                d.published_date.isoformat() 
                                    if d.published_date else None
            }
 


        #     # WRITE JSON

            directory.mkdir(parents=True, exist_ok=True) 
            with (directory / f"{d.slug}.json").open("w", encoding="utf-8") as f:
                json.dump(post_data, f, indent=2) 
        print("POST END")
    else:
        print("NO TYPE PASSED")

def loadit(self, slug=None, type=None, all=None):
    if type == "page":
        data = ''
        # print(f"DIRECTORY: {directory}")
        # print(f"SLUG:{slug}")
        if slug is not None:
            process_page(file=slug)
            
        else:
            print("Load everything")
            directory = Path("transport/pages")

            for file in directory.rglob("*.json"):
                process_page(file=file.stem)
    else:  # Post are required.
        if slug is not None:
            process_post(file=slug)
            
        else:
            print("Load everything")
            directory = Path("transport/posts")

            for file in directory.rglob("*.json"):
                process_post(file=file.stem)

def process_page(file=None):
    directory = Path("transport/pages")

    with (directory / f"{file}.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
        # print(data)
    
        obj, created = Page.objects.update_or_create(
            slug=file,
            defaults={
                "title": data['title'],
                "content": data['content'],
                "status": data["status"],
                "created": data["created"],
                "updated": data["updated"]
                },
        )

def process_post(file=None):
    directory = Path("transport/posts")
    with (directory / f"{file}.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
        author = User.objects.get(username=data['author'])
        obj, created = Post.objects.update_or_create(
            slug=file,
            defaults={
                "title": data['title'],
                "content": data['content'],
                "excerpt": data['excerpt'],
                "status": data["status"],
                "created": data["created"],
                "updated": data["updated"],
                "published_date": data["published_date"],
                "allow_comments": data["allow_comments"],
                "author": author
                },
        )
        if created is True:
            print(f"{data['title']} Created")
        else:
            print(f"{obj} Updated")