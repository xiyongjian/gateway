
import sys
import os

print('\n'.join(sys.path))

print("environment variables : %s"%str(os.environ).replace(",", "\n"))

for y in range(2000, 2017) :
    print("hello, %d"%y)