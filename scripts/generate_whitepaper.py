import argparse
import os
import shutil
from glob import glob
from os import path
from subprocess import CalledProcessError, run
from typing import cast

from bs4 import BeautifulSoup

ROOT_DIR = path.abspath(path.dirname(path.dirname(__file__)))
OUTPUT_FILE = "_includes/whitepaper.html"

REMOVED_IMAGES = []


def check_pandoc():
    try:
        run(["pandoc", "-h"], check=True, capture_output=True)
    except CalledProcessError as ex:
        raise RuntimeError(f"pandoc is not available: {ex}") from ex


def check_convert():
    try:
        run(["convert", "-h"], check=True, capture_output=True)
    except CalledProcessError as ex:
        raise RuntimeError(
            f"convert (from imagemagick) is not available: {ex.stderr}") from ex


def convert_pdf(input_file: str, output_file: str):
    try:
        run(["convert", input_file, output_file],
            check=True, capture_output=True)
    except CalledProcessError as ex:
        raise RuntimeError(
            f"failed to convert {input_file} to {output_file}: {ex.stderr}") from ex


def copy_images(base_dir: str):
    for input_file in glob(path.join(base_dir, "figures/**/*.*"), recursive=True):
        output_file = path.join(ROOT_DIR, path.relpath(input_file, base_dir))
        os.makedirs(path.dirname(output_file), exist_ok=True)
        if input_file .endswith(".pdf"):
            convert_pdf(input_file, output_file.replace(".pdf", ".png"))
        else:
            shutil.copy(input_file, output_file)


def compile_latex_to_html(base_dir: str) -> str:
    args = [
        "pandoc",
        "--from",
        "latex",
        "--bibliography",
        path.join("bib", "references.bib"),
        "--citeproc",
        "--to",
        "html5",
        "--template",
        path.join(ROOT_DIR, "misc", "pandoc-template.html5"),
        "--csl",
        path.join(ROOT_DIR, "misc", "ieee.csl"),
        "-i",
        path.join(ROOT_DIR, "misc", "pandoc-override.tex"),
        "main.tex",
    ]
    try:
        return run(args, capture_output=True, check=True, cwd=base_dir).stdout.decode("utf-8")
    except CalledProcessError as ex:
        raise RuntimeError(
            f"failed to compile document with {ex.cmd}: code {ex.returncode}, stderr {ex.stderr}") from ex


def postprocess_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, features="html.parser")
    for table in soup.find_all("table"):
        table["class"] = "table"

    for img in soup.find_all("img"):
        del img["style"]

    for embed in soup.find_all("embed"):
        embed["src"] = embed["src"].replace(".pdf", ".png")
        embed.name = "img"
        del embed["style"]

    for img in soup.find_all("img"):
        if img["src"] in REMOVED_IMAGES:
            img.parent.decompose()

    for div in soup.find_all("div", {"class": "csl-entry"}):
        div["class"] += ["row"]
    for div in soup.find_all("div", {"class": "csl-right-inline"}):
        div["class"] += ["col-11"]

    return cast(str, soup.prettify()).replace("\n", "\n      ").strip()


def main():
    parser = argparse.ArgumentParser(prog="generate-whitepaper")
    parser.add_argument("dir", help="Path to whitepaper base directory")

    args = parser.parse_args()
    check_pandoc()
    check_convert()

    copy_images(args.dir)
    raw_html = compile_latex_to_html(args.dir)
    processed_html = postprocess_html(raw_html)
    with open(OUTPUT_FILE, "w") as f:
        f.write(processed_html)


if __name__ == "__main__":
    main()
