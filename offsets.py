from requests import get
 
class Client:
    def __init__(self):
        try:
            self.offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
            self.clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client.dll.json').json()
        except:
            print('Unable to get offsets.')
            exit()
    def offset(self, a):
        try:
            return self.offsets['client.dll'][a]
        except:
            raise Exception(f'Unable to get {a}.')
            exit()
    def get(self, a, b):
        try:
            return self.clientdll['client.dll']['classes'][a]['fields'][b]
        except:
            raise Exception(f'Unable to get {a}.{b}.')
            exit()