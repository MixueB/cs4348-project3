import os
from file_parser import Parser
from btree import BTree

current_btree = None
current_file_name = None

def create_command():
    global current_btree, current_file_name
    file_name = input("Enter the name of the new index file: ").strip()
    if os.path.exists(file_name):
        overwrite = input("File exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            return
    current_btree = BTree([], 0, 1)
    current_file_name = file_name
    
    save_data()
    
    print(f"New index file '{file_name}' created and opened.")

def open_command():
    global current_btree, current_file_name
    file_name = input("Enter the name of the index file to open: ").strip()
    if not os.path.exists(file_name):
        print("Error: File does not exist.")
        return
    try:
        parser = Parser()
        current_btree = parser.parse_file(file_name)
        current_file_name = file_name
        print(f"Index file '{file_name}' opened successfully.")
    except ValueError as e:
        print(f"Error: {e}")

def insert_command():
    global current_btree, current_file_name
    if not current_btree:
        print("No index file is currently open.")
        return
    try:
        key = int(input("Enter the key: ").strip())
        value = int(input("Enter the value: ").strip())
        current_btree.insert(key, value)
        save_data()
        print(f"Key-value pair ({key}, {value}) inserted.")
    except ValueError as e:
        print(f"Error: {e}")
    except NotImplementedError as e:
        print(f"Error: {e}")

def search_command():
    global current_btree
    if not current_btree:
        print("No index file is currently open.")
        return
    try:
        key = int(input("Enter the key to search for: ").strip())
        result = current_btree.search(key)
        if result:
            print(f"Found key: {result[0]}, value: {result[1]}")
        else:
            print("Error: Key not found.")
    except ValueError:
        print("Error: Invalid input. Key must be an integer.")

def load_command():
    global current_btree
    if not current_btree:
        print("No index file is currently open.")
        return
    file_name = input("Enter the name of the file to load: ").strip()
    if not os.path.exists(file_name):
        print("Error: File does not exist.")
        return
    try:
        with open(file_name, "r") as f:
            for line in f:
                key, value = map(int, line.strip().split(","))
                
                if (not current_btree.search(key)):
                    current_btree.insert(key, value)
        save_data()
        print(f"Loaded data from '{file_name}' into the index file.")
    except Exception as e:
        print(f"Error loading file: {e}")

def print_command():
    global current_btree
    if not current_btree:
        print("No index file is currently open.")
        return
    for node in current_btree.nodes.values():
        for key, value in zip(node.keys, node.values):
            print(f"{key}, {value}")

def extract_command():
    global current_btree
    if not current_btree:
        print("No index file is currently open.")
        return
    file_name = input("Enter the name of the file to save to: ").strip()
    if os.path.exists(file_name):
        overwrite = input("File exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            return
    try:
        with open(file_name, "w") as f:
            for node in current_btree.nodes.values():
                for key, value in zip(node.keys, node.values):
                    f.write(f"{key},{value}\n")
        print(f"Data extracted to '{file_name}'.")
    except Exception as e:
        print(f"Error extracting data: {e}")

def save_data():
    global current_btree
    
    with open(current_file_name, "wb") as f:
        f.write(current_btree.serialize())

def main():
    while True:
        print("----------------------\nProject 3 Menu\n----------------------")
        print(" create\n open\n insert\n search\n load\n print\n extract\n quit\n")
        command = input("Enter a command: ").strip().lower()
        if command == "create":
            create_command()
        elif command == "open":
            open_command()
        elif command == "insert":
            insert_command()
        elif command == "search":
            search_command()
        elif command == "load":
            load_command()
        elif command == "print":
            print_command()
        elif command == "extract":
            extract_command()
        elif command == "quit":
            print("\nExiting the program")
            break
        else:
            print("Command is invalid\n")

if __name__ == "__main__":
    main()
