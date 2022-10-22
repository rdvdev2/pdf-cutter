from pdf2image import convert_from_path
import img2pdf
import os
import sys


def detect_borders(image):
    width, _ = image.size
    # left, right, top, bottom
    borders = [[0, 0, 0, 0], [0, 0, 0, 0]]

    num = 0
    pos = 0

    while (num < 6):
        x = pos%width
        y = int(pos/width)
        
        if num == 2 or num == 5:
            while image.getpixel((x, y)) == (0, 0, 0):
                x = pos%width
                y = int(pos/width)

                pos += width

            borders[int(num/3)][3] = y
            num += 1

        if num == 1 or num == 4:
            while image.getpixel((x, y)) == (0, 0, 0):
                x = pos%width
                y = int(pos/width)

                pos += 1

        
            borders[int(num/3)][1] = x

            pos -= 3
            num += 1

        if num == 0 or num == 3:
            if image.getpixel((x, y)) == (0, 0, 0):
                num += 1
                borders[int(num/3)][0] = x
                borders[int(num/3)][2] = y

            if x*2 > width:
                pos += int(width/2)

        pos += 1

    return borders



def convert_file(filename):
    print("Working with file: " + filename)
    images = convert_from_path(filename)

    filename_path_data = filename.split("/")
    filename = filename_path_data[len(filename_path_data) - 1]

    path_img = "images/" + filename

    if os.path.exists(path_img):
        os.system("rm -rf " + path_img)

    os.mkdir(path_img)

    print("Getting borders of slides...")
    borders = detect_borders(images[0])

    print(borders)

    image_files = []

    print("Cropping pages...")
    for i in range(len(images)):
        images[i].save(path_img + "/img_first_" + str(i) + ".jpg", "JPEG")

        image_up = images[i]

        image_down = image_up.copy()

        image_up_name = path_img + "/img_" + str(i*2) + ".jpg"
        image_files.append(image_up_name)
        image_up.crop((borders[0][0], borders[0][2], borders[0][1],
                       borders[0][3])).save(image_up_name, "JPEG")

        image_down_name = path_img + "/img_" + str(i*2 + 1) + ".jpg"
        image_files.append(image_down_name)
        image_down.crop((borders[1][0], borders[1][2], borders[1][1],
                       borders[1][3])).save(image_down_name, "JPEG")

    print("Saving pdf...")
    with open("result/" + filename, "wb") as f:
        f.write(img2pdf.convert(image_files))
        f.close()

    print("Ended with file: " + filename)
    print("------------------------")


if __name__ == "__main__":
    if os.path.exists("images"):
        os.system("rm -rf images")

    if not os.path.exists("result"):
        os.mkdir("result")

    os.mkdir("images")

    for file in sys.argv[1::]:
        convert_file(file)

    os.system("rm -rf images/")

