from bs4 import BeautifulSoup
import pandas as pd

# membaca file
def read_bps_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "lxml")

    rows = []
    for row in soup.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    df = pd.DataFrame(rows)

    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    return df

def create_summary(df):
    # bersihkan data
    df['status'] = df['status'].astype(str).str.strip()
    df['evaluasi'] = df['evaluasi'].astype(str).str.strip()
    df['nama'] = df['nama'].astype(str).str.strip()

    # total data per nama
    total = df.groupby('nama').size()

    # jumlah Submit
    submit_cnt = df[df['status'].str.lower() == 'submitted'].groupby('nama').size()

    # jumlah Approved
    approved_cnt = df[df['status'].str.lower() == 'approved'].groupby('nama').size()

    # selain Open
    non_open_cnt = df[df['status'].str.lower() != 'open'].groupby('nama').size()

    # selain Konsisten
    non_konsisten_cnt = df[df['evaluasi'].str.lower() != 'konsisten'].groupby('nama').size()

    # gabungkan
    pivot = pd.DataFrame({
        'Total': total,
        'Submit_Count': submit_cnt,
        'Approved_Count': approved_cnt,
        'Non_Open_Count': non_open_cnt,
        'Non_Konsisten_Count': non_konsisten_cnt
    }).fillna(0)

    # persen
    pivot['Submit_%'] = (pivot['Submit_Count'] / pivot['Total'] * 100).round(2)
    pivot['Approved_%'] = (pivot['Approved_Count'] / pivot['Total'] * 100).round(2)
    pivot['Non_Open_%'] = (pivot['Non_Open_Count'] / pivot['Total'] * 100).round(2)

    # hasil akhir
    final_pivot = pivot[['Submit_%', 'Approved_%', 'Non_Open_%', 'Non_Konsisten_Count']]

    return final_pivot.reset_index()