from graphpipe import remote
import os
import numpy as np
import cv2


class PrepareClasses:
    def __init__(self, path_to_class_file):
        self.classes = self.read_classes_from_file(path_to_class_file=path_to_class_file)

    @staticmethod
    def read_classes_from_file(path_to_class_file: str) -> list:
        assert path_to_class_file, "Path to file can't be empty!"

        _classes = []

        with open(path_to_class_file) as file:
            for _class in file.readlines():
                _classes.append(_class)

        return _classes

    def get_class_description(self, class_id):
        _class_desc = "Class does not exist..."

        try:
            _class_desc = self.classes[class_id]
        except (IndexError, TypeError) as e:
            print(e)

        _class_desc = f"[{class_id}] {_class_desc}"

        return _class_desc


class ImageUtil:

    @staticmethod
    def prepare_image(path_to_image: str):
        image = cv2.imread(path_to_image)
        image = cv2.resize(image, (227, 227))
        image = image.reshape([1] + list(image.shape))
        image = np.rollaxis(image, 3, 1).astype(np.float32)

        return image


if __name__ == "__main__":
    # get classes description
    classes_dir = os.path.join("models", "squeezenet_classes.txt")
    classes_util = PrepareClasses(path_to_class_file=classes_dir)

    images_dir = os.path.join("test_data")

    # iterate images from path
    for img in os.listdir(images_dir):
        if img.lower().endswith(('png', 'jgp')):
            _img_path = os.path.join(images_dir, img)
            _img = ImageUtil.prepare_image(_img_path)
            _classification = remote.execute("http://127.0.0.1:9000", _img)
            _class_id = np.argmax(_classification, axis=1)[0]
            _description_class_id = classes_util.get_class_description(_class_id)

            print(f"For {_img_path} classification is: {_description_class_id}")
