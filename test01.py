
import sys
import os

print('\n'.join(sys.path))

print("environment variables : %s"%str(os.environ).replace(",", "\n"))
