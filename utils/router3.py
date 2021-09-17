import router

r = router.router('192.168.10.12')
r.connect("192.168.10.13")
print("connecting done")
r.listen()
print("listening done")