import cv2
from hand_tracking import Tracker
from calculator import Button, draw_calculator

cap = cv2.VideoCapture(0)  # Open default webcam
cap.set(3, 1920) # Set width 
cap.set(4, 1080)

cv2.namedWindow("Virtual Calculator", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Virtual Calculator", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

tracker = Tracker()
equation = ''
result = ''
delay = 0  # Delay to avoid multiple rapid detections

# display box matching draw_calculator() layout
start_x = 400
display_x = start_x
display_y = 10
display_w = 30 * 5  # spacing * 5
display_h = 130 - display_y

font = cv2.FONT_HERSHEY_COMPLEX
font_scale = 1
font_thickness = 2
font_color = (255, 255, 255)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image horizontally
    img = tracker.hand_landmark(img)
    img, button_list = draw_calculator(img)
    img, dist, x1, y1 = tracker.tracking(img)  # Track index finger & get position + distance

    for button in button_list:
        if button.check_click(img, dist, x1, y1) and delay == 0:
            if button.value == 'DEL':
                if equation in ['', 'error']:
                    equation = ''
                else:
                    equation = equation[:-1] # Remove last character
                delay = 1
            elif button.value == '^':
                if equation == 'error':
                    equation = ''
                equation += '**'
                delay = 1
            elif button.value == 'CLEAR':
                equation = ''
                delay = 1
            elif button.value == '=':
                if equation not in ['', 'error']:
                    try:
                        equation = str(eval(equation))
                    except:
                        equation = 'error'
                delay = 1
            else:
                if equation == 'error':
                    equation = ''
                equation += button.value
                delay = 1

    if delay:
        delay += 1
        if delay > 10:
            delay = 0

    # Calculate text size for right alignment
    text_size = cv2.getTextSize(equation, font, font_scale, font_thickness)[0]
    text_x = display_x + display_w - text_size[0] - 10  # Right-align with 10px padding
    text_y = display_y + display_h - 30  # Vertical position inside display box

    cv2.putText(img, equation, (text_x, text_y), font, font_scale, font_color, font_thickness)

    cv2.imshow('Virtual Calculator', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
