from __future__ import print_function
import click
import os
import re
from . import api as face_recognition
import multiprocessing
import itertools
import sys
import PIL.Image
import numpy as np
import json
from json import JSONEncoder
import cv2

Encoding_dir = '../'

isPresent = True
known_people_folder=Encoding_dir
isPresent=False
cpus=1
tolerance=0.55
show_distance=False

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def scan_known_people(known_people_folder, isPresent):
    if isPresent == False:
        # Scan the faces and get encodings
        known_names = []
        known_face_encodings = []

        encoding_dict = dict()

        for file in image_files_in_folder(known_people_folder):
            basename = str(os.path.splitext(os.path.basename(file))[0])
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)
            if len(encodings) > 1:
                click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

            if len(encodings) == 0:
                click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_names.append(basename)
                known_face_encodings.append(encodings[0])
                encoding_dict[basename] = list(encodings[0])
        # Storing the encodings on a JSON file, which can be encrypted.
        # The base images can hence be deleted.
        if not os.path.exists(Encoding_dir):
            os.mkdir(Encoding_dir)
        with open(os.path.join(Encoding_dir, "enc1.json"), "w") as enc:
            enc.write(json.dumps(encoding_dict))
        return known_names, known_face_encodings
    else:
        # Load directly from directory
        with open(os.path.join(known_people_folder, "enc1.json"), "r") as enc:
            encodings = json.loads(enc.read())
        known_names = []
        known_face_encodings = []
        for k, v in encodings.items():
            known_names.append(k)
            known_face_encodings.append(np.asarray(v))
        return known_names, known_face_encodings

def print_result(filename, name, distance, show_distance=False):
    new_name = filename.rsplit('/',1)
    if show_distance:
        print("{},{},{}".format(new_name[1], name, distance))
    else:
        print("{},{}".format(new_name[1], name))


def test_image(image_to_check, known_names, known_face_encodings, tolerance=0.55, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)
    values = {}
    ctr = 0
    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            #[print_result(image_to_check, name, distance, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
            for is_match, name, distance in zip(result, known_names, distances):
            	if is_match:
            		values[ctr] = name
            		ctr = ctr + 1#list_of_people = list_of_people + " " +name
        else:
            values[ctr] = "unknown_person"
            ctr=ctr+1
            #list_of_people = list_of_people + " unknown_person"
            #print_result(image_to_check, "unknown_person", None, show_distance)

    if not unknown_encodings:
        values[ctr] = "no_person_found"
        ctr=ctr+1
        #list_of_people = list_of_people + " no person found"
        #print_result(image_to_check, "no_persons_found", None, show_distance)

    return values

def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    )

    pool.starmap(test_image, function_parameters)

def do_recognition():
    '''
    :param known_people_folder: (Required) Folder containing person's facial information. Either raw images, or precomputed encodings
    :param images_to_check: (Required) Path to image/directory of images to apply recognition alogrithm on.
    :param isPresent: (Optional) Boolean, tells if the encodings are already calculated and stored.
    :param cpus: (Optional) No of cpus to allocate. Enables multiprocessing for faster computations
    :param tolerance: (Optional) Threshold value
    :param show_distance: (Optional) Boolean, if True, shows the distance (difference) between test image and image in the database
    '''
    images_to_check = "/Users/sagban/cisco-mdm/mdm_backend/app/face_recognition/Faces/faces_to_test/img1.jpg"
    known_names, known_face_encodings = scan_known_people(known_people_folder, False)
    ret = test_image(images_to_check, known_names, known_face_encodings, tolerance, show_distance)
    return ret


def main():
    BASE_DIR = os.path.join(".", "Faces")
    #known_people_folder = input("Enter the folder where known faces/encodings are present: ")
    images_to_check = input("Enter the image on which recognition is to be applied: ")

    #known_people_folder = os.path.join(BASE_DIR, known_people_folder)
    images_to_check = os.path.join(BASE_DIR, images_to_check)
    image = cv2.imread(images_to_check)
    result = do_recognition(images_to_check)
    print(result)


if __name__ == "__main__":
    main()
