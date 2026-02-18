"""
Generating SUMMARY.md file with a list of project markdown files.
"""

import os
import re


def extract_title(file_path):
    """
    Извлекает первый заголовок H1 (# Заголовок) из markdown-файла.
    :param file_path: Путь к markdown-файлу.
    :return: Текст заголовка или None, если заголовок не найден.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
    except (IOError, UnicodeDecodeError):
        pass
    return None


def create_simple_summary(directory="."):
    """
    Creates a SUMMARY.md file with a flat list of all markdown files.
    Files from subdirectories are listed at root level with their paths.
    :param directory: The root dir to scan for MD files and subdirs (defaults to current directory).
    :return: None
    """
    summary = ["# Summary\n\n"]

    def collect_files(current_dir):
        """
        Recursively collects all markdown files, skipping hidden files, SUMMARY.md and README.md.
        :param current_dir: The current directory path to process.
        :return: List of tuples (relative_path, title)
        """
        files = []

        for item in sorted(os.listdir(current_dir)):
            if item.startswith('.') or item in ('SUMMARY.md', 'README.md'):
                continue

            full_path = os.path.join(current_dir, item)
            rel_path = os.path.relpath(full_path, directory)

            if os.path.isdir(full_path):
                # Collect files from subdirectory
                for fmd in sorted(os.listdir(full_path)):
                    if fmd.endswith('.md') and fmd not in ('SUMMARY.md', 'README.md'):
                        md_file_path = os.path.join(full_path, fmd)
                        title = extract_title(md_file_path)

                        if title:
                            files.append((rel_path.replace('\\', '/') + '/' + fmd, title))
                        else:
                            clean_name = re.sub(r'^\d+\.\s*', '', fmd[:-3])
                            files.append((rel_path.replace('\\', '/') + '/' + fmd, clean_name))
            elif item.endswith('.md'):
                title = extract_title(full_path)

                if title:
                    files.append((rel_path.replace('\\', '/'), title))
                else:
                    file_name = re.sub(r'^\d+\.\s*', '', item[:-3])
                    files.append((rel_path.replace('\\', '/'), file_name))

        return files

    # Collect all files from root and subdirectories
    all_files = collect_files(directory)
    all_files.sort(key=lambda x: x[0])

    # Write flat list
    for path, title in all_files:
        summary.append(f"- [{title}]({path})\n")

    with open(os.path.join(directory, 'SUMMARY.md'), 'w', encoding='utf-8') as f:
        f.write(''.join(summary))

    print("SUMMARY.md has been created successfully!")
    print(''.join(summary))


if __name__ == "__main__":
    target_dir = input("Enter path (Enter for current): ").strip() or "."
    create_simple_summary(target_dir)
