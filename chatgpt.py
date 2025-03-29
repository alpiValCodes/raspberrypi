import ST7735
from PIL import Image
import time

# Initialize both displays with different CS and DC pins
disp1 = ST7735.ST7735(
    port=0, 
    cs=0,  # CS for display 1
    dc=9,  # DC for display 1
    backlight=18, 
    rotation=0, 
    spi_speed_hz=4000000
)

disp2 = ST7735.ST7735(
    port=0, 
    cs=1,  # CS for display 2
    dc=6,  # DC for display 2
    backlight=23, 
    rotation=0, 
    spi_speed_hz=4000000
)

# Start both displays
disp1.begin()
disp2.begin()

# Clear both screens
img_black = Image.new('RGB', (disp1.width, disp1.height), (0, 0, 0))
disp1.display(img_black)
disp2.display(img_black)

time.sleep(0.5)  # Small delay to ensure both are cleared

# Load different images for each display
img1 = Image.open("image1.jpg").resize((disp1.width, disp1.height))
img2 = Image.open("image2.jpg").resize((disp2.width, disp2.height))

# Display different images on each screen
disp1.display(img1)
disp2.display(img2)

print("Both displays are working!")
