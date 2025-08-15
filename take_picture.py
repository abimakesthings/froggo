def take_picture(camera,timestamp,number):
    picture_path = f"images/{timestamp}_0{number}.jpg"
    camera.capture_file(picture_path)
    return picture_path
     
