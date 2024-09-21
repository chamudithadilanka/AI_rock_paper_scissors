import random
import threading
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from playsound import playsound
import os


resource_dir = "resources"

def load_img(file_name):
    image_path = os.path.join(resource_dir,file_name)
    img = cv2.imread(image_path)
    return img

def load_sound(file_name):
    sound_path = os.path.join(resource_dir, file_name)
    return sound_path

bg_image = load_img("bg2.jpg")
bg2_image = load_img("bg2.jpg")
bg3_image = load_img("bg2.jpg")


def open_new_win():
        # cv2.imshow("You Win!", imgbg2)
        # cv2.waitKey(0)  # Wait indefinitely for any key press
        # cv2.destroyAllWindows()

        # After the window is closed, play the winner video
        winner_video_path = "video/winning gif.mp4"  # Replace this with the path to your video file
        winner_video = cv2.VideoCapture(winner_video_path)

        while winner_video.isOpened():
            ret, frame = winner_video.read()
            if not ret:
                break

            cv2.imshow("Winner Video", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):  # Press 'q' to exit the video
                    break

        winner_video.release()
        cv2.destroyAllWindows()

def open_new_los():
        cv2.imshow("You Loss Try Again!", imgbg3)
        cv2.waitKey(0)  # Wait indefinitely for any key press
        cv2.destroyAllWindows()

def play_sound(sound_file):
    threading.Thread(target=lambda: playsound(sound_file)).start()

def open_game_about():
        cv2.imshow("About Game", about)
        cv2.waitKey(0)  # Wait indefinitely for any key press
        cv2.destroyAllWindows()





capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]

# Load sound files
win_score_sound = "winSound.wav"
complete_game = "complete.wav"
loss_score_sound = "lossSound.wav"
no_complete = "n.wav"



while True:

    imgbg2 = cv2.imread("resources/bg2.jpg")
    imgbg3 = cv2.imread("resources/bg3.jpg")
    imgbg = cv2.imread("resources/bg.jpg")
    about = cv2.imread("resources/about.jpg")

    success,img = capture.read()
    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgbg,str(int(timer)),(610,500),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNumber = random.randint(1,3)
                    imgAI = cv2.imread(f'resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                    imgbg = cvzone.overlayPNG(imgbg,imgAI,(149,300))

                    # Update scores
                    if (playerMove == 1 and randomNumber == 3) or \
                       (playerMove == 2 and randomNumber == 1) or \
                       (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        play_sound(win_score_sound)  # Play sound for player scoring


                    if (playerMove == 3 and randomNumber == 1) or \
                       (playerMove == 1 and randomNumber == 2) or \
                       (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        play_sound(loss_score_sound)

                    # Check if score is 5 and display popup
                    if scores[0] == 5:
                        play_sound(no_complete)
                        open_new_los()
                        #cv2.putText(imgbg, "AI WIN THE MATCH!", (300, 180), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 4)
                        cv2.imshow("bg", imgbg)
                        cv2.waitKey(2000)  # Wait for 3 seconds
                        startGame = False
                        scores = [0, 0]

                    elif scores[1] == 5:
                        play_sound(complete_game)
                        open_new_win()
                        #cv2.putText(imgbg, "PLAYER WIN THE MATCH!", (300, 180), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 4)
                        cv2.imshow("bg", imgbg)
                        cv2.waitKey(2000)  # Wait for 3 seconds
                        startGame = False
                        scores = [0, 0]


    imgbg[225:645,783:1183] = imgScaled

    if stateResult:
        imgbg = cvzone.overlayPNG(imgbg,imgAI,(100,210))

    cv2.putText(imgbg,str((scores[0])),(430,180),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.putText(imgbg,str((scores[1])),(1110,180),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)

    cv2.imshow("bg",imgbg)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False
    if key == ord('q'):
        break
    if key == ord('a'):
        open_game_about()
        startGame = True
        intialTime = time.time()



cv2.destroyAllWindows()
capture.release()
