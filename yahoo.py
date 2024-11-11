import sys

def auth(name, password):
    print('name:', name)
    users = [
        {'id': 1, 'name': 'wataru', 'password': 'password'},
        {'id': 2, 'name': 'taro', 'password': '12345678'},
        {'id': 3, 'name': 'jiro', 'password': 'abcdefgh'},
        {'id': 4, 'name': 'saburo', 'password': 'password'},
    ]

    result = list(filter(lambda x: x['name'] == name and x['password'] == password, users))

    if (result):
        return result[0]['id']
    else:
        return 'ユーザー該当なし'

if __name__ == '__main__':
    print(auth(sys.argv[1], sys.argv[2]))