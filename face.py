import argparse
from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image,ImageDraw
import cv2
import numpy as np
DEFULT_ENCODING_PATH = Path("output/encodings.pkl")
BOUNDING_BOX_COLOR="blue"
TEXT_COLOR="white"
Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)

def agraparse_parser():
    parser = argparse.ArgumentParser(description="Recognize faces in an image")
    parser.add_argument("--train", action="store_true", help="Train on input data")
    parser.add_argument(
        "--validate", action="store_true", help="Validate trained model"
    )
    parser.add_argument(
        "--test", action="store_true", help="Test the model with an unknown image"
    )
    parser.add_argument(
        "--test_cam", action="store_true", help="Test the model with an unknown image from  the camera"
    )
    parser.add_argument(
        "--video", action="store_true", help="Test the model with an unknown image from  the camera"
    )
    parser.add_argument(
        "-m",
        action="store",
        default="hog",
        choices=["hog", "cnn"],
        help="Which model to use for training: hog (CPU), cnn (GPU)",
    )
    parser.add_argument(
        "-f", action="store", help="Path to an image with an unknown face"
    )
    return  parser.parse_args()

def image_input():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Camera Feed', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
           
            path = f"saved_image.png"
            image= cv2.imwrite(f'{path}', frame)
            print("Image saved as 'saved_image.png'")
            break
    cap.release()
    cv2.destroyAllWindows()
    return path 

def encoding_known_face(model:str="hog",encodings_location:Path=DEFULT_ENCODING_PATH)->None:
   names=[]

   encodings=[]

   for filepath in Path("training").glob("*/*"):

        name=filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image,face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

   name_encodings = {"names":names,"encodings":encodings}
   
   with encodings_location.open(mode="wb")as f :
        pickle.dump(name_encodings,f)

def recognize_faces(image_location:str,model="hog",encodings_location:Path=DEFULT_ENCODING_PATH )->None:
    
    with encodings_location.open(mode='rb')as f:

        loaded_encodings = pickle.load(f)
    
    input_image= face_recognition.load_image_file(image_location)
    input_face_locatin = face_recognition.face_locations(input_image,model=model)
    input_face_encodings = face_recognition.face_encodings(input_image,input_face_locatin)
    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)
    for bounding_box,unknow_encoding in zip(input_face_locatin,input_face_encodings):

        name = _recognize_face(unknow_encoding,loaded_encodings)
        if not name :
            name="Unknow"
        _displau_face(draw,bounding_box,name)
    del draw
    pillow_image.show()

def recognize_faces_cam(model="hog",encodings_location:Path=DEFULT_ENCODING_PATH )->None:
    image_location = image_input()
    with encodings_location.open(mode='rb')as f:

        loaded_encodings = pickle.load(f)
    
    input_image= face_recognition.load_image_file(image_location)
    input_face_locatin = face_recognition.face_locations(input_image,model=model)
    input_face_encodings = face_recognition.face_encodings(input_image,input_face_locatin)
    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)
    for bounding_box,unknow_encoding in zip(input_face_locatin,input_face_encodings):

        name = _recognize_face(unknow_encoding,loaded_encodings)
        if not name :
            name="Unknow"
        _displau_face(draw,bounding_box,name)
    del draw
    pillow_image.show()

def _displau_face(draw,bounding_box,name):
    top,right,bottom,left=bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name)
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill="blue",
        outline="blue",
    )
    draw.text(
        (text_left, text_top),
        name,
        fill="white",
    )


def _recognize_face(unknow_encoding, loaded_encodings):

    boolean_matches= face_recognition.compare_faces(loaded_encodings['encodings'], unknow_encoding)
    votes = Counter(
        name
        for match,name in zip(boolean_matches,loaded_encodings["names"])
        if match 
    )
    if votes:
        return votes.most_common(1)[0][0]

def validate(model: str = "hog"):
    for filepath in Path("validation").rglob("*"):
        if filepath.is_file():
            recognize_faces(
                image_location=str(filepath.absolute()), model=model
            )

if __name__ == "__main__":
    args=agraparse_parser()
    if args.train:
        encoding_known_face(model=args.m)
    if args.validate:
        validate(model=args.m)
    if args.test:
        recognize_faces( image_location=args.f,model=args.m)
    if args.test_cam:
        recognize_faces_cam(model=args.m)
    