import requests
import csv
import os
import sys
from pathlib import Path
from PIL import Image
from io import BytesIO


def config():
    try:
        image_url_file = sys.argv[1]
    except: 
        print("\nMust enter a filepath argument.\n\nFor example: python3 app.py path/to/file.csv\n")
        sys.exit()

    # check that file is a .csv
    if not os.path.isfile(image_url_file):
        print("\nOOPS!\nFile not found. Please check filepath and try again.\n\nFor example: \n  Mac - /users/username/path/to/file.csv\n  PC - C://path/to/file.csv\n")
        sys.exit()

    # check file is a .csv
    if not image_url_file.endswith('.csv'):
        print("\nInvalid filetype. Please use a .csv file.\n")
        sys.exit()
        

    project = input("Name of project: ") # get the name of the project to set the directory names
    resized_dir = f'{project}_resized'
    og_dir = f'{project}_images'

    return resized_dir, og_dir, image_url_file


def set_width():
    # width to resize images to (height is dynamic to preserve aspect ratio). Asks for user input. Validates int and > 0.
    while True:
        basewidth = input("Set base width for resize: ")
        try:
            int(basewidth)
            if int(basewidth) > 0:
                basewidth = int(basewidth)
                break
            else: 
                print("Value must be > 0. Please try again. ")
        except:
            print("Must enter an integer > 0. Please try again.")
    
    return basewidth
    
    
def resize(resized_dir, og_dir, image_url_file, basewidth):
    # Open the CSV file containing the list of URLs
    with open(image_url_file, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header row

        # Create a directory to save the original and resized images in
        if not os.path.exists(resized_dir):
            os.makedirs(resized_dir)
        if not os.path.exists(og_dir):
            os.makedirs(og_dir)

        # Loop through each row in the CSV file
        for row in reader:
            url = row[0] # extract the URL

            # Use the requests module to download the image from the URL
            response = requests.get(url)
            print(response.status_code)

            # Open the image using Pillow
            img = Image.open(BytesIO(response.content))

            if img.size[0] > basewidth: # only resize if original image is larger than reized will be

                img.save(f'{Path.cwd()}/{og_dir}/' + url.split('/')[-1]) # save the original image

                wpercent = (basewidth / float(img.size[0])) # calculate % of original width
                hsize = int((float(img.size[1]) * float(wpercent))) # multiply height by width % to preserve aspect ratio

                img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS) # resize the image

                img.save(f'{Path.cwd()}/{resized_dir}/' + url.split('/')[-1], optimize=True) # save the resized image
            else:
                print("Original image width is equal to or less than basewidth for resize.")