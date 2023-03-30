import argparse
import os
import sys
from collections import defaultdict

import tiktoken

def get_token_count(file_path, encoding):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tokens = encoding.encode(content)
        return len(tokens), None
    except UnicodeDecodeError:
        return None, f"Skipping '{file_path}' due to a UnicodeDecodeError."

def has_files_with_tokens(path, token_counts_map):
    if path in token_counts_map:
        return True
    if os.path.isdir(path):
        children = sorted(os.listdir(path))
        for child in children:
            child_path = os.path.join(path, child)
            if has_files_with_tokens(child_path, token_counts_map):
                return True
    return False

def sort_children_by_tokens(children, path, token_counts_map):
    sorted_children = []
    for child in children:
        child_path = os.path.join(path, child)
        if child_path not in token_counts_map:
            continue
        sorted_children.append({
            'child': child,
            'tokens': token_counts_map[child_path],
        })
    return sorted(sorted_children, key=lambda x: x['tokens'], reverse=True)

def count_folder_tokens(path, token_counts_map):
    total_tokens = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            total_tokens += token_counts_map.get(file_path, 0)
    return total_tokens

def sort_folders_by_tokens(folders, base_path, token_counts_map):
    folder_info_list = []
    
    for folder_name in folders:
        folder_path = os.path.join(base_path, folder_name)
        folder_token_count = count_folder_tokens(folder_path, token_counts_map)
        folder_info_list.append({
            'folder_name': folder_name,
            'token_count': folder_token_count
        })
        
    return sorted(folder_info_list, key=lambda x: x['token_count'], reverse=True)

def print_tree_structure(path, token_counts_map, depth=0):
    if not has_files_with_tokens(path, token_counts_map):
        return

    folder_tokens = None
    if os.path.isdir(path):
        folder_icon = "📂"
        folder_tokens = count_folder_tokens(path, token_counts_map)
        print(f'{"│   " * (depth - 1)}├── {folder_icon} {os.path.basename(path)} ({folder_tokens} tokens)')

    if path in token_counts_map:
        print(f'{"│   " * (depth - 1)}├── {os.path.basename(path)}: {token_counts_map[path]} tokens')

    if os.path.isdir(path):
        children = sorted(os.listdir(path))
        dir_children = [child for child in children if os.path.isdir(os.path.join(path, child))]
        file_children = [child for child in children if os.path.isfile(os.path.join(path, child))]
        
        sorted_dir_children = sort_folders_by_tokens(dir_children, path, token_counts_map)
        for folder_info in sorted_dir_children:
            child_path = os.path.join(path, folder_info['folder_name'])
            print_tree_structure(child_path, token_counts_map, depth + 1)
            
        sorted_file_children = sort_children_by_tokens(file_children, path, token_counts_map)
        for child in sorted_file_children:
            child_path = os.path.join(path, child['child'])
            print_tree_structure(child_path, token_counts_map, depth + 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get token count for every file in a directory.")
    parser.add_argument("directory", type=str, help="Directory containing the files.")
    parser.add_argument("--encoding", type=str, default="cl100k_base", help="Encoding name (default: cl100k_base)")
    args = parser.parse_args()

    skipped_files = 0
    token_counts_map = defaultdict(int)
    if not os.path.exists(args.directory):
        print(f"Directory '{args.directory}' does not exist.")
        sys.exit(1)

    encoding = tiktoken.get_encoding(args.encoding)

    for root, dirs, files in os.walk(args.directory):
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv']]
        for file in files:
            file_path = os.path.join(root, file)
            if '.git' not in file_path and 'venv' not in file_path:
                token_count, skip_reason = get_token_count(file_path, encoding)
                if skip_reason is None and token_count > 0:
                    token_counts_map[file_path] = token_count
                elif skip_reason is not None:
                    skipped_files += 1

    print(f"Number of skipped files: {skipped_files}\n")

    print_tree_structure(args.directory, token_counts_map)
