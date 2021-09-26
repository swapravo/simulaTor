from sys import argv
from utils import router

self_ip = argv[1]
key = argv[2]
server_ip = argv[3]


r = router.router(argv[1], argv[2])
r.connect(argv[3])
print("exit connected to server")
r.listen()
print("exit connected to middle")
