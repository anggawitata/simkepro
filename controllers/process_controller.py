import os
from models.data_model import read_bps_file, create_summary

UPLOAD_FOLDER = "uploads"
LAST_FILE = os.path.join(UPLOAD_FOLDER, "last_file")

def save_file(file):
    import os
    import shutil

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # paksa nama tetap
    ext = os.path.splitext(file.filename)[1].lower()
    last_path = os.path.join(UPLOAD_FOLDER, "last_file" + ext)

    shutil.copy(filepath, last_path)

    print("SAVED:", last_path)

    return filepath


def get_last_file():
    import os

    if not os.path.exists(UPLOAD_FOLDER):
        return None

    files = os.listdir(UPLOAD_FOLDER)

    # filter file yang mengandung "last_file"
    last_files = [f for f in files if "last_file" in f]

    if not last_files:
        return None

    # ambil file pertama
    last_file = last_files[0]

    return os.path.join(UPLOAD_FOLDER, last_file)


def process_file(filepath):
    df = read_bps_file(filepath)

    summary_df = create_summary(df)

    summary_table = summary_df.to_html(
        classes='table table-bordered table-striped table-hover',
        index=False
    )

    return summary_table