from resize import *


if __name__ == "__main__":
    config = config()
    
    resized_dir = config[0]
    og_dir = config[1]
    image_url_file = config[2]

    basewidth = set_width()

    resize(resized_dir, og_dir, image_url_file, basewidth)