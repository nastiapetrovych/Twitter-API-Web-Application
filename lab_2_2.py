import sys
import json


def reading_file(name):
    """
    The function, which gets the path to json file or dictionary based on it. It calls recursive function
    :param name: str
    :return:
    """
    if isinstance(name, str):
        with open(name, 'r', encoding='utf -8') as file:
            data = json.load(file)
    if isinstance(name, dict):
        data = name
    working_with_data(data)


def working_with_data(item):
    """
    Recursive function which helps to move in json file with help of console
    :param item: dictionary
    :return: None
    """
    if isinstance(item, list):
        print(f'The  list looks like: {item}')
        print(f'The length of list is {len(item)}')
        users_request = input('Enter the index of this list\nWrite "exit" to quit: ')
        if users_request == 'exit':
            sys.exit()
        if not users_request.isdigit() or int(users_request) < 0 or int(users_request) >= len(item):
            print('The wrong index')
            working_with_data(item)
        else:
            print(item[int(users_request)])
            working_with_data(item[int(users_request)])
    if isinstance(item, dict):
        print(f'The  dictionary looks like: {item}')
        final = []
        for key in item:
            final.append(key)
        print(f'The available keys {final}')
        write1 = input('What key do u want to get?\nWrite "exit" if you want to quit: ')
        if write1 == 'exit':
            sys.exit()
        try:
            print(item[write1])
            working_with_data(item[write1])
        except KeyError:
            print("This key doesn't exist")
            working_with_data(item)
    if isinstance(item, str) or isinstance(item, int):
        print("It's the last item")
        while True:
            users_request = input('Print "exit" to finish\n')
            if users_request == 'exit':
                print('Bye')
                sys.exit()
