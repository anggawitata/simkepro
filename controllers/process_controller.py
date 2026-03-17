import os
from models.data_model import read_bps_file, create_summary

# Folder untuk menyimpan file upload
UPLOAD_FOLDER = "uploads"

# Fungsi untuk menyimpan file dari user
def save_file(file):
    # Pastikan folder uploads ada
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Gunakan nama asli file (atau bisa kamu ubah)
    filename = file.filename

    # Path lengkap file
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Simpan file
    file.save(filepath)

    return filepath


# Fungsi untuk memproses file (seperti di Colab)
def process_file(filepath):
    df = read_bps_file(filepath)

    # tabel preview (seperti sebelumnya)
    preview_table = df.head(10).to_html(
        classes='table table-bordered table-striped table-hover',
        index=False
    )

    # tabel monitoring (ringkasan)
    summary_df = create_summary(df)

    summary_table = summary_df.to_html(
        classes='table table-bordered table-striped table-hover',
        index=False
    )

    return preview_table, summary_table