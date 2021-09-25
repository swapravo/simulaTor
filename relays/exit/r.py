from sys import argv
from utils import router

print("supplied args:")
print(argv)

r = router.router(argv[1])
r.connect(argv[2])
print("exit connected to server")
r.listen()
print("exit connected to middle")
