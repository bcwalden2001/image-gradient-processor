import cv2
import numpy as np

# read in an image in opencv
image = cv2.imread("cones1.png")
image_grayscale = cv2.imread("cones1.png", 0)

# get size of an image
num_rows = image.shape[0] # height of image
num_cols = image.shape[1] # width of image

# used to scale the dimensions of the original image up by 1.5
scalingFactor = 1.5

# the new dimensions of the scaled image based on the scalingFactor, rounded to the nearest integer
num_scaled_rows = round(num_rows * scalingFactor)
num_scaled_cols = round(num_cols * scalingFactor)

# create a second image, of the same size as the original
empty_image = np.zeros( (num_rows, num_cols, 3), np.float32)

# create scaled empty image of the original image
scaled_image = np.zeros( (num_scaled_rows, num_scaled_cols, 3), np.float32)

# iterate over all the pixels in the image
for i in range(num_rows): # height of the image, y coordinates
    for j in range(num_cols): # width of the image, x coordinates

        # Steps to build new image:
        # 1. Find the starting pixel coordinate to build the centered image at
        # 2. Transfer the original pixels over into the new image's center and apply an offset for each pixel

        # image[i][j][0]: blue channel at location row i, col j
        # image[i][j][1]: green channel at location row i, col j
        # image[i][j][2]: red channel at location row i, col j

        # RGB pixels copied into empty image
        empty_image[i][j][0] = image[i][j][0]
        empty_image[i][j][1] = image[i][j][1]
        empty_image[i][j][2] = image[i][j][2]

        # Row and column to build the centered image at
        starting_row = (num_scaled_rows - num_rows) // 2
        starting_col = (num_scaled_cols - num_cols) // 2

        # copy the blue channel into the empty image with an offset to center the image
        scaled_image[i+starting_row][j+starting_col][0] = empty_image[i][j][0]

        # copy the green channel into the empty image with an offset to center the image
        scaled_image[i+starting_row][j+starting_col][1] = empty_image[i][j][1]

        # copy the red channel into empty the image with an offset to center the image
        scaled_image[i+starting_row][j+starting_col][2] = empty_image[i][j][2]

# display new/larger image in RGB 
cv2.imshow("Displaying cones1_RGB_centered.png", scaled_image/255.0)

# save to RGB image to disk
cv2.imwrite("cones1_RGB_centered.png", scaled_image)

# re-assign the scaled image to a single channel
scaled_image = np.zeros( (num_scaled_rows, num_scaled_cols), np.float32)

# iterate over all the pixels in the image and limit the range of rows and columns by one to avoid edges causing an out-of-bounds error
for i in range(1,num_rows-1): # height of the image, y coordinates
    for j in range(1,num_cols-1): # width of the image, x coordinates

        gradient_intensity = abs(float(image_grayscale[i + 1][j]) - float(image_grayscale[i - 1][j]))
        scaled_image[i + starting_row][j + starting_col] = gradient_intensity

print(f"Dimensions of three channel, original image: {image.shape[0]} x {image.shape[1]}")
print(f"Dimensions of single channel, scaled image: {scaled_image.shape[0]} x {scaled_image.shape[1]}")

# define the border regions relative to the centered image
top_border_start = starting_row
top_border_end = starting_row + num_rows
left_border_start = starting_col
left_border_end = starting_col + num_cols

# add a one-pixel border only around the centered image without affecting the upscaled image
scaled_image[top_border_start - 1:top_border_start, left_border_start:left_border_end] = 128  # Top border
scaled_image[top_border_end:top_border_end + 1, left_border_start:left_border_end] = 128  # Bottom border
scaled_image[top_border_start:top_border_end, left_border_start - 1:left_border_start] = 128  # Left border
scaled_image[top_border_start:top_border_end, left_border_end:left_border_end + 1] = 128  # Right border

# display new/larger image in greyscale showing the gradient
cv2.imshow("demo image, greyscale, Y-direction gradient, upscaled, border", scaled_image/255.0)

# save gradient image to disk
cv2.imwrite("cones1_greyscale_Y_gradient_centered.png", scaled_image)

cv2.waitKey(0) # not going to proceed until you hit "enter"
cv2.destroyAllWindows() # closes all windows opened with "imshow"
