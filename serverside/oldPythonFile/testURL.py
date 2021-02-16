from PIL import Image
import urllib.request

imgurl = 'https://static.toiimg.com/photo/72975551.cms'
print(type(imgurl))
if (imgurl.startswith('http') or imgurl.startswith('https')):
    print('true')
else:
    print('false')

with urllib.request.urlopen(imgurl) as url:
    with open('temp.jpg', 'wb') as f:
        f.write(url.read())

img = Image.open('temp.jpg')
# print(type(img))
img.show()