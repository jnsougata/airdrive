from src.__init__ import *

bh = BlackHole.login(username='issei', password='12345678')
content = bh.cache('test.mp4')
print(type(content))

