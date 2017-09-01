import sys

from requests import HTTPError

import UploadFile
import UserInterface

if __name__ == '__main__':

    try:
        class_id = UserInterface.get_course()
        assign_id = UserInterface.get_assignment(class_id)
        if not assign_id:
            sys.exit()
        file_name = UserInterface.get_file()
        if not file_name:
            sys.exit()
        UploadFile.upload_file(class_id, assign_id, file_name)
    except HTTPError:
        print(
            "Canvas returned an error. Please try again later.",
            file=sys.stderr)
        sys.exit()

    print("\nAssignment submitted.")
