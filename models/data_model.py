import pandas as pd

def read_bps_file(file_path):
    # cek isi file (bukan cuma ekstensi)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(500).lower()

    # ========================
    # HTML (termasuk XLS palsu dari Excel)
    # ========================
    if "<html" in content or "<table" in content:
        from bs4 import BeautifulSoup

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "lxml")

        rows = []
        for row in soup.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            if cells:
                rows.append(cells)

        if not rows:
            raise ValueError("File tidak mengandung tabel")

        df = pd.DataFrame(rows)

        if df.empty:
            raise ValueError("File kosong")

        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)

    # ========================
    # Excel asli
    # ========================
    else:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
        except Exception:
            raise ValueError("File bukan Excel valid atau tidak didukung")

    # ========================
    # VALIDASI
    # ========================
    if df.empty:
        raise ValueError("File kosong atau tidak terbaca")

    df.columns = df.columns.astype(str).str.strip().str.lower()

    required_cols = ['status', 'evaluasi', 'nama']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di file")

    return df


def create_summary(df):
    df['status'] = df['status'].astype(str).str.strip().str.lower()
    df['evaluasi'] = df['evaluasi'].astype(str).str.strip().str.lower()
    df['nama'] = df['nama'].astype(str).str.strip()

    total = df.groupby('nama').size()
    submit_cnt = df[df['status'] == 'submitted'].groupby('nama').size()
    approved_cnt = df[df['status'] == 'approved'].groupby('nama').size()
    non_open_cnt = df[df['status'] != 'open'].groupby('nama').size()
    non_konsisten_cnt = df[df['evaluasi'] != 'konsisten'].groupby('nama').size()

    pivot = pd.DataFrame({
        'Total': total,
        'Submit_Count': submit_cnt,
        'Approved_Count': approved_cnt,
        'Non_Open_Count': non_open_cnt,
        'Non_Konsisten_Count': non_konsisten_cnt
    }).fillna(0)

    pivot['Submit_%'] = (pivot['Submit_Count'] / pivot['Total'] * 100).round(2)
    pivot['Approved_%'] = (pivot['Approved_Count'] / pivot['Total'] * 100).round(2)
    pivot['Non_Open_%'] = (pivot['Non_Open_Count'] / pivot['Total'] * 100).round(2)

    final_pivot = pivot[['Submit_%', 'Approved_%', 'Non_Open_%', 'Non_Konsisten_Count']]

    return final_pivot.reset_index()