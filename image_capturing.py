from os import listdir, path, getcwd, mkdir
import shutil
import cv2


# Constants
train_videos_path = "./videos/train"
train_images_path = "./images/train"
test_videos_path = "./videos/test"
test_images_path = "./images/test"
capture_per_video = 4


def create_dir(frame_dir):
    if path.isdir(frame_dir):
        shutil.rmtree(frame_dir)
    try:
        mkdir(frame_dir)
    except OSError:
        print("Creation of the directory %s failed." % frame_dir)
        raise


def do_capturing(videos_path, images_path):
    create_dir(images_path)
    for video in sorted(listdir(videos_path)):
        if not '.avi' in video:
            continue
        print(video)
        vidcap = cv2.VideoCapture(path.join(videos_path, video))
        frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

        for capture in range(0, capture_per_video):
            capturing_frame = int(frame_count / (capture_per_video + 1)) * (capture + 1)
            if capturing_frame >= frame_count:
                capturing_frame = frame_count - 1

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
            print("Capturing image: " + image_name)
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