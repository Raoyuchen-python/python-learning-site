from PIL import Image, ImageDraw
import os

# 创建一个16x16的图标
img = Image.new('RGB', (16, 16), color='#3776ab')
draw = ImageDraw.Draw(img)

# 在图标上画一个简单的"P"
draw.text((4, 2), "P", fill=(255, 255, 255))

# 保存为favicon.ico
img.save('static/images/favicon.ico', format='ICO', sizes=[(16, 16)])

# 也可以生成多个尺寸
img32 = img.resize((32, 32), Image.Resampling.LANCZOS)
img.save('static/images/favicon.ico', format='ICO', 
         sizes=[(16, 16), (32, 32)])

print("favicon.ico 已生成在 static/images/ 目录")