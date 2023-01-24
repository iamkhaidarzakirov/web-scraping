import json


def test():

    with open('myProxies.json', 'r', encoding='utf-8') as file:
        proxies = json.load(file)
        print(proxies)


if __name__ == '__main__':
    test()


