import streamlit as st
import csv
import requests
import io
from collections import defaultdict, OrderedDict

# ----------------------
# Mapping kode kitab → nama lengkap kitab
# ----------------------
book_map = {
    "Kej": "Kejadian", "Kel": "Keluaran", "Ima": "Imamat", "Bil": "Bilangan", "Ula": "Ulangan",
    "Yos": "Yosua", "Hak": "Hakim-hakim", "Rut": "Rut", "1Sa": "1 Samuel", "2Sa": "2 Samuel",
    "1Ra": "1 Raja-raja", "2Ra": "2 Raja-raja", "1Ta": "1 Tawarikh", "2Ta": "2 Tawarikh",
    "Ezr": "Ezra", "Neh": "Nehemia", "Est": "Ester", "Ayb": "Ayub", "Mzm": "Mazmur", "Ams": "Amsal",
    "Pkh": "Pengkhotbah", "Kid": "Kidung Agung", "Yes": "Yesaya", "Yer": "Yeremia", "Rat": "Ratapan",
    "Yeh": "Yehezkiel", "Dan": "Daniel", "Hos": "Hosea", "Yoe": "Yoel", "Amo": "Amos", "Oba": "Obaja",
    "Yun": "Yunus", "Mik": "Mikha", "Nah": "Nahum", "Hab": "Habakuk", "Zef": "Zefanya", "Hag": "Hagai",
    "Zak": "Zakharia", "Mal": "Maleakhi",
    "Mat": "Matius", "Mrk": "Markus", "Luk": "Lukas", "Yoh": "Yohanes", "Kis": "Kisah Para Rasul",
    "Rom": "Roma", "1Ko": "1 Korintus", "2Ko": "2 Korintus", "Gal": "Galatia", "Efe": "Efesus",
    "Flp": "Filipi", "Kol": "Kolose", "1Te": "1 Tesalonika", "2Te": "2 Tesalonika",
    "1Ti": "1 Timotius", "2Ti": "2 Timotius", "Tit": "Titus", "Flm": "Filemon", "Ibr": "Ibrani",
    "Yak": "Yakobus", "1Pt": "1 Petrus", "2Pt": "2 Petrus", "1Yo": "1 Yohanes", "2Yo": "2 Yohanes",
    "3Yo": "3 Yohanes", "Yud": "Yudas", "Why": "Wahyu"
}

# ----------------------
# Urutan kitab Alkitab
# ----------------------
canonical_books = [
    "Kejadian", "Keluaran", "Imamat", "Bilangan", "Ulangan",
    "Yosua", "Hakim-hakim", "Rut", "1 Samuel", "2 Samuel",
    "1 Raja-raja", "2 Raja-raja", "1 Tawarikh", "2 Tawarikh",
    "Ezra", "Nehemia", "Ester", "Ayub", "Mazmur", "Amsal",
    "Pengkhotbah", "Kidung Agung", "Yesaya", "Yeremia", "Ratapan",
    "Yehezkiel", "Daniel", "Hosea", "Yoel", "Amos", "Obaja",
    "Yunus", "Mikha", "Nahum", "Habakuk", "Zefanya", "Hagai",
    "Zakharia", "Maleakhi",
    "Matius", "Markus", "Lukas", "Yohanes", "Kisah Para Rasul",
    "Roma", "1 Korintus", "2 Korintus", "Galatia", "Efesus",
    "Filipi", "Kolose", "1 Tesalonika", "2 Tesalonika", "1 Timotius",
    "2 Timotius", "Titus", "Filemon", "Ibrani", "Yakobus",
    "1 Petrus", "2 Petrus", "1 Yohanes", "2 Yohanes", "3 Yohanes",
    "Yudas", "Wahyu"
]

# ----------------------
# URL GitHub raw
# ----------------------
CSV_URL = "https://raw.githubusercontent.com/AlvinWinarta2111/Bible-App/main/data/tb.csv"
CROSS_URL = "https://raw.githubusercontent.com/AlvinWinarta2111/Bible-App/main/assets/cross.png"
SIDEBAR_URL = "https://raw.githubusercontent.com/AlvinWinarta2111/Bible-App/main/assets/sidebar.png"

# ----------------------
# Top Banner
# ----------------------
st.image(CROSS_URL, use_container_width=True)

# ----------------------
# Load CSV dari URL
# ----------------------
bible_data = defaultdict(lambda: defaultdict(dict))

response = requests.get(CSV_URL)
response.raise_for_status()
csvfile = io.StringIO(response.text)

reader = csv.DictReader(csvfile)
reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

for row in reader:
    row = {k.strip().lower(): v.strip() for k, v in row.items()}
    book_code = row.get('kitab', '')
    book = book_map.get(book_code, book_code)
    chapter = row.get('pasal', '')
    verse = row.get('ayat', '')
    text = row.get('firman', '')
    if book and chapter and verse and text:
        bible_data[book][chapter][verse] = text

# ----------------------
# Sort kitab, pasal, ayat
# ----------------------
bible_data_ordered = OrderedDict()
for book in canonical_books:
    if book in bible_data:
        chapters_sorted = OrderedDict(sorted(bible_data[book].items(), key=lambda x: int(x[0])))
        chapters_sorted_sorted_verses = OrderedDict()
        for ch, verses in chapters_sorted.items():
            verses_sorted = OrderedDict(sorted(verses.items(), key=lambda x: int(x[0])))
            chapters_sorted_sorted_verses[ch] = verses_sorted
        bible_data_ordered[book] = chapters_sorted_sorted_verses

# ----------------------
# Sidebar
# ----------------------
st.sidebar.image(SIDEBAR_URL, width=250)
st.sidebar.title("📖 Filter Alkitab")

selected_book = st.sidebar.selectbox("Pilih Kitab", [""] + list(bible_data_ordered.keys()))

selected_chapter = ""
verse_start = None
verse_end = None
if selected_book:
    chapters = list(bible_data_ordered[selected_book].keys())
    selected_chapter = st.sidebar.selectbox("Pilih Pasal", [""] + chapters)

    if selected_chapter:
        verses = [int(v) for v in bible_data_ordered[selected_book][selected_chapter].keys()]
        if verses:
            min_verse = min(verses)
            max_verse = max(verses)
            col1, col2 = st.sidebar.columns(2)
            with col1:
                verse_start = st.number_input("Ayat", min_value=min_verse, max_value=max_verse, value=min_verse, step=1)
            with col2:
                verse_end = st.number_input("Sampai Ayat", min_value=min_verse, max_value=max_verse, value=max_verse, step=1)

# ----------------------
# Tampilan utama
# ----------------------
if selected_book and selected_chapter:
    st.header(f"{selected_book} Pasal {selected_chapter}")

    verses_all = bible_data_ordered[selected_book][selected_chapter]

    # 1️⃣ Ayat terpilih di atas
    if verse_start is not None and verse_end is not None:
        st.subheader("Ayat Terpilih")
        for v_num_str, v_text in verses_all.items():
            v_num = int(v_num_str)
            if verse_start <= v_num <= verse_end:
                st.markdown(
                    f"<div style='background-color: #fff9b0; padding:5px; border-radius:3px;'>"
                    f"<b>{v_num}</b>. {v_text}</div>",
                    unsafe_allow_html=True
                )

    # 2️⃣ Seluruh pasal dengan highlight pada ayat terpilih
    st.subheader("Seluruh ayat di pasal ini")
    for v_num_str, v_text in verses_all.items():
        v_num = int(v_num_str)
        if verse_start is not None and verse_end is not None and verse_start <= v_num <= verse_end:
            st.markdown(
                f"<div style='background-color: #fff9b0; padding:2px; border-radius:3px;'>"
                f"<b>{v_num}</b>. {v_text}</div>",
                unsafe_allow_html=True
            )
        else:
            st.write(f"{v_num}. {v_text}")

    st.markdown("---")

else:
    st.write("👈 Silakan pilih kitab, pasal, dan rentang ayat dari sidebar untuk menampilkan ayat.")
