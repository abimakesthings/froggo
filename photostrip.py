from PIL import Image
#stack the 3 images vertically into one photostrip
def merge(im1, im2, im3) -> Image.Image: #importing image paths
    im1 = Image.open(im1)
    im2 = Image.open(im2)
    im3 = Image.open(im3)

    w = 12 + im1.size[0] + 12 #12px margins
    h = 12 + im1.size[1] + 12 + im2.size[1] + 12 + im3.size[1] + 12 #12px gap and margins
    im = Image.new("RGBA", (w, h))

    im.paste(im1, (12,12))
    im.paste(im2, (12, im1.height + 24))
    im.paste(im3, (12, im1.height + im2.height + 36))

    im = im.convert("1", dither=Image.Dither.FLOYDSTEINBERG) #dithering for thermal printing
   
    return im