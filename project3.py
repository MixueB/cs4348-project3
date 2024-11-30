

def create_command():
    pass
    
def open_command():
    pass
    
def insert_command():
    pass
    
def search_command():
    pass
    
def load_command():
    pass
    
def print_command():
    pass
    
def extract_command():
    pass

while True:
    print('----------------------\nProject 3 Menu\n----------------------')
    print(' create\n open\n insert\n search\n load\n print\n extract\n quit\n')
    command = input('Enter a command: ')
    
    if command == 'create':
        create_command()
    elif command == 'open':
        open_command()
    elif command == 'insert':
        insert_command()
    elif command == 'search':
        search_command() 
    elif command == 'load':
        load_command()
    elif command == 'print':
        print_command()
    elif command == 'quit':
        print('\nExiting the program')
        break
    else:
        print('Command is invalid\n')