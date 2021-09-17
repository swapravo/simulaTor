import router

r = router.router('192.168.10.11')
r.connect('192.168.10.12')
print("connecting done")
r.listen()
print("listening done")