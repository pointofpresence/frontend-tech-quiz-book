"""
Generating SUMMARY.md file with a list of project markdown files.
"""

import os
import re


def create_simple_summary(directory="."):
    """
    Creates a SUMMARY.md file in the specified directory by recursively scanning for markdown files
    and organizing them into a hierarchical table of contents.
    :param directory: The root dir to scan for MD files and subdirs (defaults to current directory).
    :return: None
    """
    summary = ["# Summary\n\n"]

    def process_dir(current_dir, level=0):
        """
        Recursively processes a directory to build a markdown summary tree of markdown files
        and subdirectories, skipping hidden files and SUMMARY.md.
        :param current_dir: The current directory path to process.
        :param level: The current indentation level for the summary tree (used for recursive calls).
        :return: None (modifies the global 'summary' list in-place).
        """
        items = []

        for item in sorted(os.listdir(current_dir)):
            if item.startswith('.') or item in ('SUMMARY.md', 'README.md'):
                continue

            full_path = os.path.join(current_dir, item)
            rel_path = os.path.relpath(full_path, directory)

            if os.path.isdir(full_path):
                md_files = [fmd for fmd in os.listdir(full_path)
                            if fmd.endswith('.md') and fmd not in ('SUMMARY.md', 'README.md')]

                if md_files:
                    folder_name = re.sub(r'^\d+\.\s*', '', item)
                    items.append((rel_path, folder_name, True, sorted(md_files)))

            elif item.endswith('.md'):
                file_name = re.sub(r'^\d+\.\s*', '', item[:-3])  # Убираем .md и нумерацию
                items.append((rel_path, file_name, False, None))

        items.sort(key=lambda x: x[0])

        for path, name, is_dir, md_files in items:
            indent = "  " * level

            if is_dir:
                if md_files:
                    first_file = os.path.join(path, md_files[0])
                    summary.append(f"{indent}- [{name}]({first_file})\n")
                    process_dir(os.path.join(directory, path), level + 1)
                else:
                    summary.append(f"{indent}- {name}\n")
            else:
                summary.append(f"{indent}- [{name}]({path})\n")

    process_dir(directory)

    with open(os.path.join(directory, 'SUMMARY.md'), 'w', encoding='utf-8') as f:
        f.write(''.join(summary))

    print("SUMMARY.md has been created successfully!")
    print(''.join(summary))


if __name__ == "__main__":
    target_dir = input("Enter path (Enter for current): ").strip() or "."
    create_simple_summary(target_dir)
