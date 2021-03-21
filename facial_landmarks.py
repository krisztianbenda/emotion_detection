import face_recognition as fr
import pandas as pd
from os import listdir, path, getcwd, mkdir


train_images_path = "./images/train"
test_images_path = "./images/test"
gathered_landmarks = ['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'left_eye', 'right_eye',
                     'top_lip', 'bottom_lip']
emotions = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']


def append_to_df(data, columns, df):
    if 'test' not in data[0]:
        for emotion in emotions:
            columns.append('is' + emotion)
            if emotion in data[0]:
                data.append(1)
            else:
                data.append(0)
    df = df.append(pd.DataFrame([data], columns=columns), ignore_index=True)
    return df


def data_extraction(images_path):
    person = ""
    data = []
    columns = ['video']
    df = pd.DataFrame()
    for image in sorted(listdir(images_path)):
        if not '.jpg' in image:
            continue
            
        if person == image.split('_')[0]:
            warned = False
            new_frame = image.split('_')[1].split('.')[0]
            new_landmarks = fr.face_landmarks(fr.load_image_file(path.join(images_path, image)))
            for gathered_landmark in gathered_landmarks:
                for idx, point in enumerate(landmarks[0][gathered_landmark]):
                    try:
                        if len(new_landmarks[0][gathered_landmark]) != len(landmarks[0][gathered_landmark]):
                            print(" WARN: can't find the proper number of points for image: " + image)
                            print(" WARN: landmark: " + gathered_landmark)
                            print(" WARN: number of points: ", len(new_landmarks[0][gathered_landmark]))
                            print(" WARN: number of expected points: ", len(landmarks[0][gathered_landmark]))
                   
                        distanceX = point[0] - new_landmarks[0][gathered_landmark][idx][0]
                        distanceY = point[1] - new_landmarks[0][gathered_landmark][idx][1]
                    
                        columns.append(str(frame_count) + '-' + str(frame_count+1) + '_' + gathered_landmark + str(idx) + 'X')
                        data.append(distanceX)

                        columns.append(str(frame_count) + '-' + str(frame_count+1) + '_' + gathered_landmark + str(idx) + 'Y')
                        data.append(distanceY)
                    except:
                        if not warned:
                            print(" WARN: can't find the proper landmarks for image: " + image)
                            print(" WARN: found landmarks: ", new_landmarks)
                            print(" WARN: searching for: " + gathered_landmark)
                            warned = True
                        columns.append(str(frame_count) + '-' + str(frame_count+1) + '_' + gathered_landmark + str(idx) + 'X')
                        data.append(0)
                        columns.append(str(frame_count) + '-' + str(frame_count+1) + '_' + gathered_landmark + str(idx) + 'Y')
                        data.append(0)
                        
            landmarks = new_landmarks
            frame = new_frame
            frame_count+=1
        else:
            if len(data) != 0:
                df = append_to_df(data, columns, df)
            person = image.split('_')[0]
            frame = image.split('_')[1].split('.')[0]
            frame_count = 0
            print(person, frame)
            landmarks = fr.face_landmarks(fr.load_image_file(path.join(images_path, image)))
            data = [person]
            columns = ['video']
            
    df = append_to_df(data, columns, df)
    return df


if __name__ == '__main__':
    df = pd.DataFrame()
    for emotion in sorted(listdir(train_images_path)):
        if not path.isdir(path.join(train_images_path, emotion)):
            continue
        print("===================")
        print("Processing emotion: " + emotion)

        df = df.append(data_extraction(path.join(train_images_path, emotion)), ignore_index=True)
        
    df.to_csv('train.csv')
    print("|=|+|+|+|+|+|+|+|++||++|+|+|")
    print("Processing test videos: ")
    df = pd.DataFrame()
    df = data_extraction(path.join(test_images_path))
    df.to_csv('test.csv')