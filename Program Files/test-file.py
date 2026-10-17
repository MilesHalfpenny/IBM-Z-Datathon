import time
hydrated=False
while True:
    hydrated=False
    while not hydrated:
        h=input("have u hydrated? (Y/N)")
        h.upper()
        if h=="Y":
            hydrated=True
    time.sleep(3600000)