def width(image):
  return image["width"]

def height(image):
  return image["height"]

def pixel(image, x, y):
  index = x + width(image)*y
  if index < 0 or index >= len(image['pixels']):
    return 0
  else:
    return image["pixels"][index]

def set_pixel(image, x, y, color):
  index = x + width(image)*y
  image["pixels"][index] = color

def make_image(width, height):
  return {"width": width, "height": height, "pixels": ([0]*width*height)}

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
  result = make_image(width(image), height(image))
  for x in range(width(result)):
    for y in range(height(result)):
      color = pixel(image, x, y)
      set_pixel(result, x, y, f(color))
  return result

# The code below seems to have some problems.
# Fix it before implementing the rest of your lab
def filter_invert(image):
  def invert(c):
    return abs(255-c)
  return apply_per_pixel(image, invert)

# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)

def apply_blur_per_pixel(image, f):
  result = make_image(width(image), height(image))
  # Kernel and coordinates for blurring
  kernel = [1.0/16, 2.0/16, 1.0/16, 2.0/16, 4.0/16, 2.0/16, 1.0/16, 2.0/16, 1.0/16]
  kernel_index = [-1, 0, 1]

  for x in range(width(result)):
    for y in range(height(result)):
      color = 0
      index_counter = 0
      # Apply kernel
      for y_i in kernel_index:
        for x_i in kernel_index:
          if (x == 0 and x_i == -1) or (x == width(image) - 1 and x_i == 1) or (y == 0 and y_i == -1) or (y == height(image) - 1 and y_i == 1):
            color += 0
          else:
            color += pixel(image, x + x_i, y + y_i) * kernel[index_counter]
          index_counter += 1
      set_pixel(result, x, y, f(color))
  return result


def filter_gaussian_blur(image):
  def pass_color(c):
    return int(round(c))
  return apply_blur_per_pixel(image, pass_color)












