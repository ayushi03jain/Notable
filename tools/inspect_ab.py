#!/usr/bin/env python3
with open('notable.ab','rb') as f:
    for i in range(10):
        line = f.readline()
        if not line:
            break
        print(repr(line))
    # also print first 64 bytes of remaining payload
    payload = f.read(64)
    print('PAYLOAD-HEAD:', payload[:64])
