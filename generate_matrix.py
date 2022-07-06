"""
Geek AGV Datamatrix Generator for Grid Localization

Author: Creed Zagrzebski (czagrzebski@gmail.com)

"""

from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageFont, ImageDraw
import sys

print("Geek Datamatrix Generator for Grid Localization")

while True:
  
    cell_id = input('Cell ID:> ')

    if(cell_id == "exit"):
        sys.exit()

    print("\nStarting Generation")

    # generate the datamatrix using encoded bytes
    data_matrix_encoded = encode(cell_id.encode('utf-8'))

    # create the image from bytes
    data_matrix_img = Image.frombytes('RGB', (data_matrix_encoded.width, data_matrix_encoded.height), data_matrix_encoded.pixels)

    # remove white pixels from generated data matrix by processing each pixel
    for i in range(0,data_matrix_img.width):
        for j in range(0,data_matrix_img.height):
            data = data_matrix_img.getpixel((i,j))
            #print(data) #(255, 255, 255)
            if (data[0]==255 and data[1]==255 and data[2]==255):
                data_matrix_img.putpixel((i,j),(244,240,223))

    print('Processing Matrix')

    # scale the image using box resample method (no blur)
    data_matrix_img = data_matrix_img.resize((280, 280), resample=Image.BOX)

    # generate the template used for the QR
    template = Image.new("RGB", size=(632, 632), color=(244,240,223))

    parent_ctr = int(template.width / 2)
    child_ctr = int(data_matrix_img.width /2 )

    template.paste(data_matrix_img, (parent_ctr - child_ctr, parent_ctr - child_ctr ))

    # create draw instance to add border, text, and alignment indicators
    draw = ImageDraw.Draw(template)

    # specify font and add text
    if(sys.platform == "win32"):
        fnt = ImageFont.truetype('arial.ttf', 50)
    else:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 50, encoding="unic")

    draw.text((20, 10), cell_id, font=fnt, fill=(0, 0, 0))
    draw.text((20, template.width - 70), "GJ", font=fnt, fill=(0, 0, 0))

    # draw alignment guides
    draw.line([(template.width / 2, 0 ), (template.width / 2, 70)], width=2, fill="BLACK")
    draw.line([(template.width, template.height / 2 ), (template.width - 70, template.height / 2)], width=2, fill="BLACK")
    draw.line([(template.width / 2, template.height ), (template.width / 2, template.height - 70)], width=2, fill="BLACK")
    draw.line([(0, template.height / 2 ), (70, template.height / 2)], width=2, fill="BLACK")

    draw.rectangle(((104, 104),(526, 526)), outline='Black', width=50)

    template.save(f'{cell_id}.jpg', quality=100)

    print('Processing Complete \n')
