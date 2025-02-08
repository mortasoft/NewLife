import os

def tree(directory, prefix=""):
    entries = sorted([e for e in os.listdir(directory) if e not in (".venv", "__pycache__")], key=str.lower)
    entries_count = len(entries)
    
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == entries_count - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)
        
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree(path, new_prefix)

if __name__ == "__main__":
    tree(".")