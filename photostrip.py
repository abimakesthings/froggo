from PIL import Image, ImageEnhance
#stack the 3 images vertically into one photostrip
def merge(im1, im2, im3) -> Image.Image: #importing image paths
    im1 = Image.open(im1)
    im2 = Image.open(im2)
    im3 = Image.open(im3)

    margin_small = 36 #36px margins
    margin_big = 64 #64px margins
    w = margin_small + im1.size[0] + margin_small 
    h = margin_big + im1.size[1] + margin_big + im2.size[1] + margin_big + im3.size[1] + margin_big*2 #marginpx gap and margins
    im = Image.new("L", (w, h), 255)

    im.paste(im1, (margin_small,margin_big))
    im.paste(im2, (margin_small, im1.height + margin_big*2))
    im.paste(im3, (margin_small, im1.height + im2.height + margin_big*3))
 
    im = im.resize((384, int(im.height * 384 / im.width))) #resize image to fit printer
    im = ImageEnhance.Contrast(im).enhance(1.2)
    im = ImageEnhance.Brightness(im).enhance(1.05)
    im = im.convert("1", dither=Image.Dither.FLOYDSTEINBERG) #dithering for thermal printing

    return im