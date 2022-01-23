# https://pillow.readthedocs.io/en/stable/reference/Image.html

import os
import sys
import logging
from PIL import Image

try:
    def file_validation():
        global fileName, filePath, img, imgWidth, imgHeight
        while True:
            if not os.path.exists("1_material"):
                os.makedirs("1_material")
            for file in os.listdir("1_material"):
                if file.endswith(".gif") or file.endswith(".png") or file.endswith(".PNG"):
                    fileName = os.path.join(file)  
                    filePath = ("1_material/") + fileName
                    img = Image.open(filePath)
                    imgWidth, imgHeight = img.size   
                    print()
                    #print("Current working dir is: " + os.getcwd())
                    print("File in use right now is " + f'"{fileName}"')
                    break  
            else:
                fileName = 0
            if fileName == 0:
                print()
                print("No file of supported format present (only .png or .gif).")
                print("Place the right file into the '1_material' folder and press the 'ENTER' key.")
                input()
                continue        
            break

    def command_validation():   
        global command, batch, previousGroup, newGroup, shift_value, previousGroupIndex
        command = input("Enter your command: [S]how, [R]eplace, [PR]ecise replace, [H]elp: ")
        while command.casefold() != "s" and command.casefold() != "r" and command.casefold() != "pr"and command.casefold() != "h":
            print()
            print("Unknown command.")
            print("Allowed commands are: [S]how, [R]eplace, [PR]ecise replace, [H]elp.")
            print()
            command = input("Enter your command: ")
        def get_group_input(prompt):
            while True:
                try:
                    value = int(input(prompt))
                except ValueError:
                    print()
                    print("Invalid input. Only numbers are allowed.")
                    continue
                if value < 0 or value > 16:
                    print()
                    print("Invalid input. Only numbers from 0 to 16 are allowed.")
                    continue
                else:
                    return value
                    break
        def get_shift_input(prompt):
            while True:
                try:
                    value = int(input(prompt))
                except ValueError:
                    print()
                    print("Invalid value. Only numbers are allowed.")
                    continue
                if value < -15 or value > 15:
                    print()
                    print("Value is too low. Only values from -15 to 15 are allowed.")
                    continue
                else:
                    return value
                    break
        if command.casefold() == "r":
            previousGroup = get_group_input("Define the colour group you want to be changed [0-16]: ")
            newGroup = get_group_input("Define the new colour group [0-16]: ")
            shift_value = get_shift_input("By how much you want to shift the hue? Type 0 if you don't. [-15 - 15]: ")
            folderPath = "1_material/"
            batch = "n"
            totalFiles = 0
            for base, dirs, files in os.walk(folderPath):
                for Files in files:
                    totalFiles += 1
            if totalFiles > 1:
                print("There are multiple files in the folder.")
                batch = input("Do you wish to shift all of the files? [y|n]: ")
                while batch != "y" and batch != "n":
                    print()
                    print("Invalid answer.")
                    batch = input("Type [y] or [n]: ")
        elif command.casefold() == "pr":
            previousGroup = get_group_input("Define the colour group you want to be changed [0-16]: ")
            newGroup = get_group_input("Define the new colour group [0-16]: ")
            previousGroupIndex = get_group_input("Define the colour index you want to be changed [0-15]: ")
            shift_value = get_shift_input("By how much you want to shift the hue? Type 0 if you don't. [-15 - 15]: ")
            folderPath = "1_material/"
            batch = "n"
            totalFiles = 0
            for base, dirs, files in os.walk(folderPath):
                for Files in files:
                    totalFiles += 1
            if totalFiles > 1:
                print("There are multiple files in the folder.")
                batch = input("Do you wish to shift all of the files? [y|n]: ")
                while batch.casefold() != "y" and batch.casefold() != "n":
                    print()
                    print("Invalid answer.")
                    batch = input("Type [y] or [n]: ")
        elif command.casefold() == "s":
            print()
            print("Printing...")
            print()
        elif command.casefold() == "h":
            print()
            print("Main commands:")
            print("[S]how - prints the coordinates, colour group and tint of every non blank pixel.")
            print("[R]eplace - shifts all pixels of defined colour group to another, additionally shifting the tint if defined.")
            print("[PR]ecise replace - shifts all pixels of defined colour group AND tint to another colour group, additionally shifting the tint if defined.")
            print("[H]elp - you are here.")

    def file_processing():
        global fileName, filePath, img, imgWidth, imgHeight
        for pixelIndex in range(0, imgWidth*imgHeight):
            PixelX = int(pixelIndex % imgWidth)
            PixelY = int(pixelIndex / imgWidth)
            pixel = int(img.getpixel((PixelX, PixelY)))
            if command.casefold() == "s":
                currentGroup = pixel // 16
                currentGroupIndex = pixel % 16
                if currentGroup != 15 and currentGroupIndex != 0:
                    print("X: {} - Y: {} - Group: {} - Tint: {}".format(PixelX, PixelY, currentGroup, currentGroupIndex))
            elif command.casefold() == "r":
                currentGroup = pixel // 16
                currentGroupIndex = pixel % 16 
                if currentGroup == previousGroup:
                    if currentGroupIndex + shift_value < 15 and currentGroupIndex + shift_value > 0:
                        currentGroupIndex = currentGroupIndex + shift_value
                    elif currentGroupIndex + shift_value >= 15:
                        currentGroupIndex = 15
                    elif currentGroupIndex + shift_value <= 0:
                        currentGroupIndex = 0
                    if currentGroup != 0 or currentGroupIndex != 0:
                        pixel = newGroup * 16 + currentGroupIndex
                    if pixel != 0:
                        img.putpixel((PixelX, PixelY), pixel)
            elif command.casefold() == "pr":
                currentGroup = pixel // 16
                currentGroupIndex = pixel % 16 
                if currentGroup == previousGroup and currentGroupIndex == previousGroupIndex:
                    if shift_value != 0:
                        currentGroupIndex = currentGroupIndex + shift_value
                    if currentGroup != 0 or currentGroupIndex != 0:
                        pixel = newGroup * 16 + currentGroupIndex
                    if pixel != 0:
                        img.putpixel((PixelX, PixelY), pixel)


    def file_release():
        global filePath 
        if command.casefold() == "r" or command.casefold() == "pr":
            if not os.path.exists("3_shifted"):
                os.makedirs("3_shifted")
            img.save("3_shifted/" + fileName, format="png")
            img.close()
            if not os.path.exists("2_used"):
                os.makedirs("2_used")
            os.replace(filePath, "2_used/"+ fileName)
            print()
            print("Done.")
            print("Shifted image saved at - 3_shifted/" + fileName)
            print("Original image is moved to - 2_used/" + fileName)   
        elif command.casefold() == "s":
            print()
            print("The format is: X and Y coordinates of the pixel - its colour group - index of its colour.")    

    def batch_process():
        if batch.casefold() == "y":
            if not os.path.exists("1_material"):
                os.makedirs("1_material")            
            for file in os.listdir("1_material"):
                if file.endswith(".gif") or file.endswith(".png") or file.endswith(".PNG"):
                    file_validation()
                    file_processing()
                    file_release()

    while True:
        file_validation()
        command_validation()
        file_processing()
        file_release()
        if command.casefold() == "r" or command.casefold() == "pr":
            batch_process()
        continue

    #print()
    #print("Press ENTER to close this window.")

    #sys.exit(0)

except:
    LOG_FILENAME = ('crashlog.txt')
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')
    logging.exception('An exception occurred.')
    raise