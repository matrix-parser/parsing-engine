from pdf2image import convert_from_path

images = convert_from_path("input.pdf")

for i in range(len(images)):
    images[i].save("page" + str(i) + ".jpg", "JPEG")
