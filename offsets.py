from requests import get as g
class Client:
    def __init__(self):
        try:
            self.offsets = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
            self.clientdll = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()
        except:
            print('Unable to get offsets.')
            exit()
    def offset(self, a):
        try:
            return self.offsets['client.dll'][a]
        except:
            print(f'Offset {a} not found.')
            exit()
    def get(self, a, b):
        try:
            return self.clientdll['client.dll']['classes'][a]['fields'][b]
        except:
            print(f'Unable to get {a}, {b}.')
            exit()
