from textnode import *
from htmlnode import *
from inline_markdown import *
from markdown_blocks import *
import os
import shutil
import pathlib


def copycontents(dir, dst):
    print(f"Clearing {dst}")
    shutil.rmtree(dst)
    print(f"Making {dst}")
    os.mkdir(dst)
    files = os.listdir(dir)
    for file in files:
        path = os.path.join(dir, file)
        if os.path.isfile(path) == True:
            print(f"{path} exists, copying to {dst} ")
            shutil.copy(path, dst)
        else:
            print(f"{path} did not exist")
            newdst = os.path.join(dst, file)
            print(f"New destination = {newdst}")
            if os.path.exists(newdst) == False:
                os.mkdir(newdst)
            print(f"Copying to {newdst}")
            copycontents(path, newdst)
    return

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line.strip("# ")
        else:
            continue
    raise Exception("Markdown should contain header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as fp:
        markdown = fp.read()
    with open(template_path, "r") as tp:
        template = tp.read()
    html = markdown_to_html_node(markdown)
    content = html.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    filename = os.path.basename(from_path).replace('.md', '.html')
    newdest = os.path.join(dest_path, filename)
    
    with open(newdest, "w") as dst:
        dst.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        path = os.path.join(dir_path_content, file)
        if os.path.isfile(path) == True:    
            generate_page(path, template_path, dest_dir_path)
        else:
            dst = os.path.join(dest_dir_path, file)
            os.makedirs(dst, exist_ok=True)
            generate_pages_recursive(path, template_path, dst)

    
def main():
    copycontents("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    return

main()
