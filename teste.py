# Rotate the image around in a circle
angle = 0
while angle <= 360:
    # Rotate the source image
    img = rotate(src, angle)    
    # Crop the center 1/3rd of the image (roi is filled with text)
    h,w = img.shape
    buffer = min(h, w) - int(min(h,w)/1.15)
    roi = img[int(h/2-buffer):int(h/2+buffer), int(w/2-buffer):int(w/2+buffer)]
    # Create background to draw transform on
    bg = np.zeros((buffer*2, buffer*2), np.uint8)
    # Compute the sums of the rows
    row_sums = sum_rows(roi)
    # High score --> Zebra stripes
    score = np.count_nonzero(row_sums)
    scores.append(score)
    # Image has best rotation
    if score <= min(scores):
        # Save the rotatied image
        print('found optimal rotation')
        best_rotation = img.copy()
    k = display_data(roi, row_sums, buffer)
    if k == 27: break
    # Increment angle and try again
    angle += .75
cv2.destroyAllWindows()