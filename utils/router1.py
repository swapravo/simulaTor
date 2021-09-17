import router

r = router.router('192.168.10.10')
r.connect('192.168.10.11')
print("connecting done")
r.listen()
print("listening done")