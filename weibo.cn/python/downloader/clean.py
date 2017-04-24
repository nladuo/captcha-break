
import os
for fn in os.listdir("./captchas/"):
    if os.path.splitext(fn)[1] == '.gif':
        os.remove("./captchas/"+fn)