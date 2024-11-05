import mss
import time
import numpy as np
import cv2
import win32gui
import win32con
import win32api

# Define capture interval (3 ticks = 23.4 ms)
interval = 23.4 / 1000  # Convert milliseconds to seconds

def find_white_pixel_center(image, whitemin,whitemax):
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    _, binary = cv2.threshold(gray, whitemin, whitemax, cv2.THRESH_BINARY)

    # Get the coordinates of all white pixels
    white_pixels = np.column_stack(np.where(binary == 255))

    # Check if there are any white pixels
    if len(white_pixels) == 0:
        return None  # No white pixels found

    # Calculate the median of the coordinates
    median_y, median_x = np.median(white_pixels, axis=0)

    return (int(median_x), int(median_y))  # Return the median as a tuple



def get_window_rect(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)
        return rect
    else:
        print(f"Window '{window_name}' not found.")
        return None
mask_img = cv2.imread("maps/ascent/ascentmask.png", cv2.IMREAD_UNCHANGED)
_, _, _, alpha_channel = cv2.split(mask_img)
alpha_channel = cv2.bitwise_not(alpha_channel)
# Main loop
with mss.mss() as sct:
    while True:
        start_time = time.time()
        
        # Get the window's position and size
        window_name = "VALORANT  "  # Use the exact window name
        rect = get_window_rect(window_name)
        
        if rect:
            left, top, right, bottom = rect
            width = right - left
            height = bottom - top
            monitor = {"top": top, "left": left, "width": width, "height": height}
            
            # Capture the specified window area
            screenshot = sct.grab(monitor)
            
            # Convert to a numpy array (for OpenCV processing)
            img = np.array(screenshot)
            
            # Optional: Convert to BGR (OpenCV format)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            
            
            # --- Process the image here (e.g., for AI inference) ---
            map = img[42:503, 18:479]
            # Apply the mask using the alpha channel (255 = keep, 0 = mask out)
            
            img_masked = cv2.bitwise_and(map, map, mask=alpha_channel)
            map =img_masked
            white_mask = cv2.inRange(img_masked, (244, 244, 244), (255, 255, 255))
            player_layer = cv2.bitwise_and(img_masked, img_masked, mask=white_mask)
            playerpos = find_white_pixel_center(player_layer,250,254)
            playeraimpos = find_white_pixel_center(player_layer,250,255)
            if playeraimpos:
                cv2.circle(player_layer, (playeraimpos[0], playeraimpos[1]), 5, (0, 0, 255), -1)  # Red color in BGR
            if playerpos:
                cv2.circle(player_layer, (playerpos[0], playerpos[1]), 5, (255, 0, 0), -1)  # Blue color in BGR
            #map zone 18, 42 // 478, 502
            '''map colors
            bomb A5A389
            bg 7E7F7E
            ally barrier 68AF9E
            enemy barrier BFBF3F'''

            
            
            

            cv2.imshow("map", player_layer)
            
            
            
            
            
            
            dscale = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            # Display for debugging
            cv2.imshow("Valorant Window Capture", dscale)

            
            # Close on 'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        # Calculate elapsed time and sleep if necessary to match interval
        elapsed_time = time.time() - start_time
        sleep_time = interval - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

# Release resources
cv2.destroyAllWindows()
