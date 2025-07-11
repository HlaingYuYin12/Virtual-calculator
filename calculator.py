import cv2
from hand_tracking import Tracker


class Button:
    def __init__(self, x, y, w, h, value,
                 font=cv2.FONT_HERSHEY_COMPLEX,
                 font_color=(255, 255, 255),
                 thick=1, font_size=0.4):
        
        # initialize button
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = value


        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.font_color = (255, 255, 255)
        self.thick = 1
        self.font_size = 0.4

        # button text style
        self.text_width, self.text_height = cv2.getTextSize(self.value, self.font, self.font_size, self.thick)[0]

    def draw(self, img):
        # draw button on frame
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h),
                      (50, 50, 50), cv2.FILLED)
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h),
                      (10, 10, 10), 3)
        # draw dark outline
        cv2.putText(img, self.value,
                    (self.x + (self.w - self.text_width) // 2,
                     self.y + (self.h + self.text_height) // 2),
                    self.font, self.font_size, self.font_color, self.thick)

        return img

    def check_click(self, img, dist, x1, y1):
        if (self.x <= x1 <= self.x + self.w) and (self.y <= y1 <= self.y + self.h) and dist <= 35:
            cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h),
                          (0, 255, 0), cv2.FILLED)
            # green fill 
            cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h),
                          (10, 10, 10), 3)
            # outline
            cv2.putText(img, self.value,
                        (self.x + (self.w - self.text_width) // 2,
                         self.y + (self.h + self.text_height) // 2),
                        self.font, self.font_size, self.font_color, self.thick)
            return True
        return False


def draw_calculator(img):
    button_list_values = [['7', '8', '9', '^', '('],
                          ['4', '5', '6', '*', ')'],
                          ['1', '2', '3', '-', 'DEL'],
                          ['0', '.', '/', '+', '=']]
    
    button_list = []
    start_x = 400
    start_y = 200
    button_w = 30
    button_h = 30
    spacing = 30

    # layout
    for i in range(4):
        for j in range(5):
            x = start_x + spacing * j
            y = start_y + spacing * i
            button_list.append(Button(x, y, button_w, button_h, button_list_values[i][j]))

    # Smaller CLEAR button
    clear_button = Button(start_x + spacing * 0, start_y + spacing * 4, 150, 40, 'CLEAR')
    button_list.append(clear_button)

    # Draw buttons
    for button in button_list:
        img = button.draw(img)

    # Smaller display area
    img = cv2.rectangle(img, (start_x, 10), (start_x + spacing * 5, 130), (50, 50, 50), cv2.FILLED)
    img = cv2.rectangle(img, (start_x, 10), (start_x + spacing * 5, 130), (10, 10, 10), 2)

    
    return img, button_list


if __name__ == "__main__":
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    tracker = Tracker()
    equation = ''
    result = ''
    delay = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1) #flip cam
        img = tracker.hand_landmark(img)
        img, button_list = draw_calculator(img)
        img, dist, x1, y1 = tracker.tracking(img)

        for button in button_list:
            if button.check_click(img, dist, x1, y1) and delay == 0:
                print('click')
            if cv2.waitKey(1) & 0xFF == 27 :
                break

        # print(x1, y1)
        # print(img.shape)
        cv2.imshow('Image', img)
        cv2.waitKey(1)