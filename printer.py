from escpos.printer import File

p = File(devfile="/dev/usb/lp0")
p.image("images/2025-07-31-20-54-14_photostrip.bmp")   # This must be B/W and small (~384px width)
p.cut()