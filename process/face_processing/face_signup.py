import numpy as np
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths


class FaceSignUp:
    def __init__(self):
        self.database = DataBasePaths()
        self.face_utilities = FaceUtils()

    def process(self, face_image: np.ndarray, user_code: str) -> Tuple[np.ndarray, bool, str]:
        # step 1: check face detection
        check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
        if check_face_detect is False:
            return face_image, False, '¡No face detected!'

        # step 2: face mesh
        check_face_mesh, face_mesh_info = self.face_utilities.face_mesh(face_image)
        if check_face_mesh is False:
            return face_image, False, '¡No face mesh detected!'

        # step 3: extract face mesh
        face_mesh_points_list = self.face_utilities.extract_face_mesh(face_image, face_mesh_info)

        # step 4: check face center
        check_face_center = self.face_utilities.check_face_center(face_mesh_points_list)

        # step 5: show state
        self.face_utilities.show_state_signup(face_image, state=check_face_center)
        if check_face_center:
            # step 6: extract face info
            face_bbox = self.face_utilities.extract_face_bbox(face_image, face_info)
            face_points = self.face_utilities.extract_face_points(face_image, face_info)

            # step 7: face crop
            face_crop = self.face_utilities.face_crop(face_save, face_bbox)

            # step 8: save face
            check_save_image = self.face_utilities.save_face(face_crop, user_code, self.database.faces)
            return face_image, check_save_image, '¡Saved face!'

        else:
            return face_image, False, 'No face center!'



