"""
Parser to create MD-file structure by categories.
Creates folders named after categories, containing article-N.md files.
"""

# pylint: disable=too-many-locals

import json
import os
import re

from transliterate import translit


def safe_translit(name: str) -> str:
    """
    Transliterates a filename/folder name: converts Cyrillic to Latin,
    replaces spaces with hyphens, and removes invalid characters.
    :param name: The original filename or folder name as a string.
    :return: A sanitized filename/folder name string with transliterated characters
    and safe characters only.
    """
    base, ext = os.path.splitext(name)
    new_base = translit(base, "ru", reversed=True)
    new_base = re.sub(r"\s+", "-", new_base)
    new_base = re.sub(r"[^a-zA-Z0-9._-]", "", new_base)

    return new_base + ext


def promote_markdown_headings(text: str) -> str:
    """
    Promotes all Markdown headings by one level.
    Example: '# Title' becomes '## Title', '## Subtitle' becomes '### Subtitle', etc.
    :param text: Input Markdown text.
    :return: Markdown text with all heading levels increased by 1.
    """

    def _replace_heading(match):
        hashes = match.group(1)
        content = match.group(2)

        # Limit to reasonable depth (e.g., don't go beyond ######)
        if len(hashes) >= 6:
            return match.group(0)  # Keep as-is if already at max level

        return '##' + hashes + ' ' + content

    # Match lines that start with 1-6 '#' followed by a space and content
    # ^ at start of line, (#+) captures the hashes, \s+ ensures at least one whitespace,
    # (.*) captures the rest of the heading text
    return re.sub(r'^(#{1,6})\s+(.*)$', _replace_heading, text, flags=re.MULTILINE)


def parse_questions(json_path, output_dir="."):
    """
    Parses a JSON file with questions and creates an MD-file structure by categories.
    :param json_path: Path to the JSON file with questions
    :param output_dir: Base directory for creating the MD file structure
    :return: None
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    with open('tags.json', 'r', encoding='utf-8') as f:
        all_tags = json.load(f)
        original_tags, display_tags = all_tags

    categories = {}

    for question in questions:
        category = question.get('category', 'Без категории')

        if category not in categories:
            categories[category] = []

        categories[category].append(question)

    # Creating a structure for each category
    for category, items in categories.items():
        # Creating a category folder
        category_slug = safe_translit(category)
        category_dir = os.path.join(output_dir, "2-" + category_slug)
        os.makedirs(category_dir, exist_ok=True)

        # Creating MD files
        created_files = []

        for idx, question in enumerate(items):
            filename = f"article-{idx + 1}.md"
            filepath = os.path.join(category_dir, filename)
            title = question.get('title', '-')
            answer = "### Краткий ответ\n\n" + promote_markdown_headings(question.get('answer', ''))
            tags = [category] + question.get('tags', [])
            display_categories = []

            for tag in tags:
                tag_index = original_tags.index(tag)
                display_category = display_tags[tag_index]
                display_categories.append(display_category)

            content = f"# {title}\n\n"

            if len(display_categories) > 0:
                content += "### Категории\n\n"
                display_categories = list(set(display_categories))
                content += ", ".join(display_categories)
                content += "\n\n"

            content += f"{answer}\n"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append((filename, title))
            print(f"Created file: {filepath}")

        print(f"Category '{category}' processed: {len(created_files)} file(s)")

    print(f"\nTotal categories: {len(categories)}")
    print("Parsing completed successfully!")


if __name__ == "__main__":
    import sys

    json_file = sys.argv[1] if len(sys.argv) > 1 else "all_questions.json"
    output_directory = sys.argv[2] if len(sys.argv) > 2 else "."

    if not os.path.exists(json_file):
        print(f"Error: file '{json_file}' not found")
        sys.exit(1)

    parse_questions(json_file, output_directory)
