from os import listdir, path, getcwd, mkdir, environ
import shutil
import cv2


# Constants
train_videos_path = "./videos/train"
train_images_path = "./images/train"
test_videos_path = "./videos/test"
test_images_path = "./images/test"
capture_per_video = int(environ['CAPTURE_PER_VIDEO'])


def create_dir(frame_dir):
    if path.isdir(frame_dir):
        shutil.rmtree(frame_dir)
    try:
        mkdir(frame_dir)
    except OSError:
        print("Creation of the directory %s failed." % frame_dir)
        raise


def get_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) < 1:
        return None, -1, -1

    for (x, y, w, h) in faces:
        # cv2.rectangle(image, (x, y), (x+w, y+h), 
        #             (0, 0, 255), 2)
        
        image = image[y-15:y + h+15, x-15:x + w+15]
        # cv2.imshow("face",faces)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, w, h
  

def do_capturing(videos_path, images_path):
    create_dir(images_path)
    for video in sorted(listdir(videos_path)):
        if not '.avi' in video:
            continue
        
        vidcap = cv2.VideoCapture(path.join(videos_path, video))
        frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        # at the first 40% of the video there is no action so it could be cut off
        useless_first_frames = int(frame_count * 0.4) + 1

        print(f"File: {video}, total frame count: {frame_count}, starting from frame: {useless_first_frames}")
        help_number = 0

        for capture in range(0, capture_per_video):
            capturing_frame = int((frame_count-useless_first_frames) / (capture_per_video + 1)) * (capture + 1) + help_number
            capturing_frame += useless_first_frames # add the first useless frames to place it appropriatly
            if capturing_frame >= frame_count:
                print(f"Captureing frame: {capturing_frame} would be higher then total frame count: {frame_count}")
                capturing_frame = frame_count - 1
                print(f"New capturing frame will be: {capturing_frame}")

            vidcap.set(cv2.CAP_PROP_POS_FRAMES, capturing_frame)
            success, image = vidcap.read()
            if not success:
                print("ERROR: can't read frame: " + str(capturing_frame) + " frame count: " + str(frame_count))

            if capturing_frame < 10:
                frame_name = '00' + str(int(capturing_frame))
            elif capturing_frame < 100:
                frame_name = '0' + str(int(capturing_frame))
            else:
                frame_name = str(int(capturing_frame))
            image_name = video.split('.avi')[0] + '_' + frame_name + '.jpg'

            image, width, height = get_face(image)
            if image is None:
                print("WARN: Cannot find face. Help will be added. help_number={}, capture={}".format(help_number, capture))
                help_number += 1
                capture -= 1
                continue
            else:
                help_number = 0
            print("Capturing image: {} with size: ({},{})".format(image_name, width, height))
            image = cv2.resize(image, (48, 48), interpolation = cv2.INTER_AREA)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path.join(images_path, image_name), image)


if __name__ == '__main__':
    # Process train videos:
    for emotion in sorted(listdir(train_videos_path)):
        if not path.isdir(path.join(train_videos_path, emotion)):
            continue
        print("===================")
        print("Processing emotion: " + emotion)
        do_capturing(path.join(train_videos_path, emotion), path.join(train_images_path, emotion))
        
    # Process test videos:
    print("|=|+|+|+|+|+|+|+|++||++|+|+|")
    print("Processing test videos: ")
    do_capturing(test_videos_path, test_images_path)