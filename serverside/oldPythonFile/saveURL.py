from PIL import Image
from urllib.request import Request, urlopen
import os
from io import BytesIO
from urllib.parse import urlparse
from os.path import splitext, basename
import shutil

imgurl = 'https://assets.simpleviewcms.com/simpleview/image/upload/c_limit,h_1200,q_75,w_1200/v1/clients/lasvegas/strip_b86ddbea-3add-4995-b449-ac85d700b027.jpg'
req = Request(imgurl,  headers={'User-Agent': 'Mozilla/5.0'})
print(type(imgurl))
if (imgurl.startswith('http') or imgurl.startswith('https')):
    print('true')
else:
    print('false')

disassembled = urlparse(imgurl)
filename, ext = splitext(basename(disassembled.path))
print(filename)
filename += '.jpg'
sourceDir = 'C:/Users/who/PycharmProjects/Project-Theia/serverside/oldPythonFile/'
dest = 'C:/Users/who/PycharmProjects/Project-Theia/serverside/oldPythonFile/Images/'

webpage = urlopen(req).read()
with open(filename, 'wb') as f:
    f.write(webpage)

# with urllib.request.urlopen(imgurl) as url:
#
#     with open(filename, 'wb') as f:
#         f.write(url.read())

img = Image.open(filename)
img.close()
path = os.path.join( sourceDir, filename)
newpath = os.path.join( dest, filename)
print(path)
shutil.move(path, newpath)



# for aws to upload it to s3
# buffered = BytesIO()
# img.save(buffered, format=img.format)
# img_str = buffered.getvalue()
#
# # img_str= img_str.decode("utf-8")


# img.show()