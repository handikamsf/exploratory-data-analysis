import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.express as px
from scipy import stats

df = pd.read_excel("data_prep.xlsx")

image1 = Image.open("logo upn2.png")
image2 = Image.open("logo tim.png")

# --- CONFIG PAGE ---
st.set_page_config(page_title="Dashboard Circle Pertemanan", layout="wide")

st.markdown("""
    <style>
    /* Ubah warna background chip multiselect */
    div[data-baseweb="tag"] {
        background-color: #3B82F6 !important;   /* biru */
        color: white !important;
    }
    /* Ubah warna tombol "X" */
    div[data-baseweb="tag"] span {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- SIDEBAR FILTER (SLICER) ---
st.sidebar.markdown("### 🎚️ <span style='color:#1E90FF'>Filter Data</span>", unsafe_allow_html=True)

# ========================
# 🔹 Fakultas Multiselect
# ========================
fakultas_list = sorted(df['Fakultas'].unique().tolist())
fakultas_options = ['Semua'] + fakultas_list

selected_fakultas = st.sidebar.multiselect(
    "Pilih Fakultas",
    fakultas_options,
    default=['Semua']  # default awal pilih semua
)

# Logika: jika 'Semua' dipilih → pakai semua fakultas
if 'Semua' in selected_fakultas:
    filtered_fakultas = fakultas_list
else:
    filtered_fakultas = selected_fakultas

# ========================
# 🔹 Program Studi Multiselect (tergantung Fakultas)
# ========================
# Ambil prodi hanya dari fakultas terpilih
prodi_list = sorted(df[df['Fakultas'].isin(filtered_fakultas)]['Program Studi'].unique().tolist())
prodi_options = ['Semua'] + prodi_list

selected_prodi = st.sidebar.multiselect(
    "Pilih Program Studi",
    prodi_options,
    default=['Semua']  # default awal pilih semua
)

if 'Semua' in selected_prodi:
    filtered_prodi = prodi_list
else:
    filtered_prodi = selected_prodi

# ========================
# ✨ Terapkan Filter ke DataFrame
# ========================
filtered_df = df[
    (df['Fakultas'].isin(filtered_fakultas)) &
    (df['Program Studi'].isin(filtered_prodi))
]

st.markdown(
    """
    <style>
    /* Warna teks tab yang belum aktif */
    .stTabs [data-baseweb="tab"] {
        color: #E2E8F0;
    }

    /* Warna tab aktif */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: white !important;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }

    /* Warna garis bawah tab aktif */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #3B82F6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard Overview",
    "📊 Analisis Deskriptif",
    "📈 Analisis Korelasi",
    "⚔️ Analisis Perbandingan Fasilkom vs Non-Fasilkom",
    "🧮 Analisis Regresi Linear Berganda"
])

with tab0:
    # ======== HEADER ========
    col1, col2, col3 = st.columns([0.11, 0.5, 0.11])

    with col1:
        st.image(image1, width=250)  # logo kiri

    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
                <h1>📊 Dashboard Circle Pertemanan </h1>
                <h3>by MEJIKUHIBINIU - UPN "Veteran" Jawa Timur</h3>
                <h7>Muhammad Handika Maulana Sifa 24083010036 | Sonya Audina Akbar 24083010013 | Siti Nur Izzati 24083010023</h7>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.image(image2, width=250)  # logo kanan

    st.markdown("<hr>", unsafe_allow_html=True)

    # ======== PENJELASAN DATA ========
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("#### 📌 Deskripsi Data")
        st.markdown(
            """
            Dataset ini merupakan hasil survei terhadap mahasiswa UPN “Veteran” Jawa Timur untuk menganalisis fenomena **circle pertemanan** dan keterkaitannya dengan **motivasi belajar**. Data mencakup **13 variabel**, yang terdiri dari:
            - Identitas responden (Fakultas, Program Studi)  
            - Kondisi circle (Jumlah Anggota, Kategori Circle)  
            - Interaksi circle (Jenis Interaksi Dominan, Frekuensi Bertemu & Belajar, Durasi Belajar)  
            - Dinamika circle (Dukungan Circle, Gangguan Akademik, Konsistensi Dukungan)  
            - Variabel motivasi (Persepsi Motivasi & Motivasi Penyelesaian Tugas)
            
            Dataset menggabungkan variabel **kategorikal dan numerik**, memungkinkan analisis komprehensif terhadap pola sosial dan akademik mahasiswa.
            """
        )

    with col5:
        st.markdown("#### 📎 Sumber Data")
        st.markdown(
            """
            Data diperoleh melalui **kuesioner online** yang disebarkan lintas fakultas dan program studi. Responden berjumlah **164 orang** berasal dari berbagai angkatan dan jurusan, memberikan gambaran beragam mengenai kondisi circle di kampus.
            """
        )

        st.markdown("#### 🎯 Tujuan Dashboard")
        st.markdown(
            """
            Dashboard ini bertujuan untuk:
            - Menyajikan **gambaran menyeluruh** mengenai pembentukan dan interaksi circle pertemanan.  
            - Menganalisis **hubungan circle** dengan **motivasi belajar** mahasiswa.  
            - Menyediakan **insight interaktif** untuk eksplorasi data secara visual sebelum analisis deskriptif lanjutan.
            """
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ======== DATA PREVIEW ========
    st.markdown("#### 📂 Data Preview")
    st.dataframe(filtered_df)

    st.markdown("---")

    # Statistik Deskriptif
    st.markdown("#### 📊 Statistik Deskriptif Fitur Numerik")
    st.dataframe(filtered_df.describe(include='number').T)
    st.markdown("---")

    st.markdown("#### 📋 Statistik Deskriptif Fitur Kategori")
    st.dataframe(filtered_df.describe(include='object').T)


    # ======== FOOTER ========
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #9fb3c8; font-size: 13px;">
            🌐 Dashboard ini dikembangkan sebagai bagian dari analisis sosial akademik berbasis data oleh tim MEJIKUHIBINIU – 2025
        </div>
        """,
        unsafe_allow_html=True
    )


with tab1:
    st.title("📊 Analisis Deskriptif")
    st.markdown(
        """
        Bagian ini menyajikan **gambaran umum responden dan pola circle pertemanan** mahasiswa melalui visualisasi data deskriptif.
        Visualisasi ini membantu memahami sebaran responden, karakteristik circle, pola interaksi, serta kondisi motivasi belajar mahasiswa.
        """
    )
    st.markdown("---")

    common_layout = dict(
    plot_bgcolor="#1e293b",
    paper_bgcolor="#1e293b",
    font=dict(color="white", family="Sans-serif", size=12),
    margin=dict(l=40, r=20, t=50, b=40)
    )

    custom_blues = [
    'rgb(33,113,181)',
    'rgb(8,81,156)',
    'rgb(8,48,107)',
    'rgb(107,174,214)',
    'rgb(158,202,225)',
    'rgb(198,219,239)',
    'rgb(222,235,247)',
    'rgb(247,251,255)',
    'rgb(66,146,198)'   # 🟦 warna awal
]


    # ======= Identitas Responden =======

    st.markdown("## 🧍 Identitas Responden")

    col1, col2 = st.columns(2)

    # Grafik Fakultas (Vertikal)
    with col1:
        fakultas_count = filtered_df['Fakultas'].value_counts().reset_index()
        fakultas_count.columns = ['Fakultas', 'Jumlah']

        fig_fakultas = px.bar(
            fakultas_count,
            x='Fakultas',
            y='Jumlah',
            color='Fakultas',
            title='Distribusi Responden per Fakultas',
            color_discrete_sequence=custom_blues
        )
        fig_fakultas.update_layout(**common_layout, xaxis={'categoryorder':'total descending'}, showlegend=False)
        st.plotly_chart(fig_fakultas, use_container_width=True)

        st.markdown(
            f"**Insight:** Total responden: **{len(filtered_df)}**. Fakultas terbanyak: **{fakultas_count.iloc[0]['Fakultas']}** ({fakultas_count.iloc[0]['Jumlah']} responden)."
        )  

    # Grafik Program Studi (Horizontal)
    with col2:
        prodi_count = filtered_df['Program Studi'].value_counts().reset_index()
        prodi_count.columns = ['Program Studi', 'Jumlah']

        fig_prodi = px.bar(
            prodi_count,
            x='Jumlah',
            y='Program Studi',
            color='Program Studi',
            title='Distribusi Responden per Program Studi',
            orientation='h',
            color_discrete_sequence=custom_blues
        )
        fig_prodi.update_layout(**common_layout, yaxis={'categoryorder':'total ascending'},showlegend=False)
        st.plotly_chart(fig_prodi, use_container_width=True)

        st.markdown(
            f"**Insight:** Program studi terbanyak: **{prodi_count.iloc[0]['Program Studi']}** ({prodi_count.iloc[0]['Jumlah']} responden)."
        )

    st.markdown("---")

    # 2. KONDISI CIRCLE
    # ---------------------------
    st.markdown("### 🫂 Kondisi Circle")
    col3, col4 = st.columns(2)

    with col3:
        # Histogram Jumlah Anggota Circle (transparan) 
        fig_jumlah_circle = px.histogram(
            filtered_df,
            x='Jumlah Anggota Circle',
            nbins=15,
            title='Sebaran Jumlah Anggota Circle',
            color_discrete_sequence=custom_blues
        )
        fig_jumlah_circle.update_layout(common_layout, showlegend=False)
        fig_jumlah_circle.update_xaxes(title_text="Jumlah Anggota")
        fig_jumlah_circle.update_yaxes(title_text="Frekuensi")
        st.plotly_chart(fig_jumlah_circle, use_container_width=True)

        # Tambahan insight jumlah anggota circle
        mean_circle_size = filtered_df['Jumlah Anggota Circle'].mean()
        median_circle_size = filtered_df['Jumlah Anggota Circle'].median()
        st.markdown(
            f"**Insight:** Rata-rata jumlah anggota circle adalah **{mean_circle_size:.1f} orang** dengan median **{median_circle_size} orang**. *Circle yang lebih besar dapat menawarkan lebih banyak dukungan sosial.*"
        )
      

    with col4:
        # Proporsi kategori circle (pie chart)
        circle_count = filtered_df['Circle Category'].value_counts().reset_index()
        circle_count.columns = ['Kategori Circle', 'Jumlah']
        fig_circle = px.pie(
            circle_count,
            names='Kategori Circle',
            values='Jumlah',
            title='Proporsi Kategori Circle',
            color_discrete_sequence=custom_blues
        )
        #color text inside pie white
        fig_circle.update_traces(textposition='inside', textinfo='percent+label')
        fig_circle.update_layout(common_layout, showlegend=False)
        st.plotly_chart(fig_circle, use_container_width=True)

        # Insight spesifik kategori
        n_resp = len(filtered_df)
        pct_small = (filtered_df['Jumlah Anggota Circle'] <= 5).mean() * 100
        top_cat = circle_count.iloc[0]
        top_cat_pct = top_cat['Jumlah'] / n_resp * 100 if n_resp > 0 else 0
        st.markdown(
            f"**Insight:** **{pct_small:.1f}%** responden memiliki circle kecil (≤5 orang). *Circle kecil cenderung lebih intim dan mendukung interaksi mendalam.*"
        )

    st.markdown("---")

    # ---------------------------
    # 3. INTERAKSI CIRCLE
    # ---------------------------
    st.markdown("### 💬 Pola Interaksi Circle")
    

    interaksi_count = filtered_df['Jenis Interaksi Dominan'].value_counts().reset_index()
    interaksi_count.columns = ['Jenis Interaksi', 'Jumlah']
    fig_interaksi = px.bar(
            interaksi_count,
            y='Jenis Interaksi',
            x='Jumlah',
            orientation='h',
            title='Jenis Interaksi Dominan dalam Circle',
            color_discrete_sequence=custom_blues,
            color='Jenis Interaksi'
        )
    fig_interaksi.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'}, **common_layout)
    fig_interaksi.update_yaxes(automargin=True)
    st.plotly_chart(fig_interaksi, use_container_width=True)

        # Insight interaksi
    top_inter = interaksi_count.iloc[0]
    top_inter_pct = top_inter['Jumlah'] / n_resp * 100 if n_resp > 0 else 0
    st.markdown(
            f"**Insight:** Interaksi terbanyak: **{top_inter['Jenis Interaksi']}** ({top_inter['Jumlah']} responden → **{top_inter_pct:.1f}%**). "
            " *Ini menunjukkan cara utama circle membangun hubungan.*"
    )
    col5, col6 = st.columns(2)

    with col5:
        # Frekuensi Bertemu (histogram)

        fig_freq_meet = px.histogram(
            filtered_df,
            x='Frekuensi Bertemu Seminggu',
            nbins=8,
            title='Sebaran Frekuensi Bertemu per Minggu',
            color_discrete_sequence=custom_blues
        )
        fig_freq_meet.update_layout(common_layout, showlegend=False)
        fig_freq_meet.update_xaxes(title_text="Kali bertemu / minggu")
        st.plotly_chart(fig_freq_meet, use_container_width=True)

        # Tambahan insight frekuensi bertemu
        mean_meet = filtered_df['Frekuensi Bertemu Seminggu'].mean()
        pct_never_meet = (filtered_df['Frekuensi Bertemu Seminggu'] == 0).mean() * 100
        st.markdown(
            f"**Insight:** Rata-rata bertemu **{mean_meet:.1f}x/minggu**. *Ini menunjukkan seberapa sering circle berinteraksi secara langsung.* "
        )

    # Frekuensi Belajar Bersama (histogram, full width)
    with col6:
        fig_freq_study = px.histogram(
            filtered_df,
            x='Frekuensi Belajar Bersama Seminggu',
            nbins=8,
            title='Sebaran Frekuensi Belajar Bersama per Minggu',
            color_discrete_sequence=custom_blues
        )
        fig_freq_study.update_layout(common_layout, showlegend=False)
        fig_freq_study.update_xaxes(title_text="Kali belajar bersama / minggu")
        st.plotly_chart(fig_freq_study, use_container_width=True)

        # Tambahan insight frekuensi belajar
        mean_study = filtered_df['Frekuensi Belajar Bersama Seminggu'].mean()
        pct_never_study = (filtered_df['Frekuensi Belajar Bersama Seminggu'] == 0).mean() * 100
        st.markdown(
            f"**Insight:** Rata-rata belajar bersama **{mean_study:.1f}x/minggu** dan sebanyak **{pct_never_study:.1f}%** responden tidak pernah belajar bersama. "
        )

    st.markdown("---")

    # ---------------------------
    # 4. DINAMIKA CIRCLE & MOTIVASI
    # ---------------------------
    st.markdown("### 🚀 Dinamika Circle & Motivasi Belajar")
    col7, col8 = st.columns(2)

    with col7:
        # Dukungan Circle (kategori)
        dukungan_count = filtered_df['Dukungan Circle'].value_counts().reset_index()
        dukungan_count.columns = ['Dukungan Circle', 'Jumlah']
        fig_dukungan = px.bar(
            dukungan_count,
            y='Dukungan Circle',
            x='Jumlah',
            orientation='h',
            title='Tingkat Dukungan Circle terhadap Akademik',
            color_discrete_sequence=custom_blues,
            color='Dukungan Circle'
        )
        fig_dukungan.update_layout(common_layout, showlegend=False, yaxis={'categoryorder':'total ascending'})
        fig_dukungan.update_yaxes(automargin=True)
        st.plotly_chart(fig_dukungan, use_container_width=True)

        # Insight dukungan
        top_support = dukungan_count.iloc[0]
        pct_top_support = top_support['Jumlah'] / n_resp * 100 if n_resp > 0 else 0
        st.markdown(
            f"**Insight:** Mayoritas melaporkan **{top_support['Dukungan Circle']}** sebagai tingkat dukungan ({pct_top_support:.1f}%). "
            " *Jika dukungan tinggi, circle kemungkinan mempercepat penyelesaian tugas.*"
        )

    with col8:
        #Gangguan Akademik pie chart
        gangguan_count = filtered_df['Gangguan Akademik'].value_counts().reset_index()
        gangguan_count.columns = ['Gangguan Akademik', 'Jumlah']
        fig_gangguan = px.pie(
            gangguan_count,
            names='Gangguan Akademik',
            values='Jumlah',
            title='Proporsi Gangguan Akademik oleh Circle',
            color_discrete_sequence=custom_blues
        )
        fig_gangguan.update_traces(textposition='inside', textinfo='percent+label')
        fig_gangguan.update_layout(common_layout, showlegend=False)
        st.plotly_chart(fig_gangguan, use_container_width=True)

        # Insight gangguan
        no_gangguan = gangguan_count[gangguan_count['Gangguan Akademik'] == 'Tidak']
        hi = no_gangguan['Jumlah'].iloc[0] / n_resp * 100 if n_resp > 0 and not no_gangguan.empty else 0
        st.markdown(
            f"**Insight:** Sebanyak **{hi:.1f}%** responden tidak merasa terganggu akademiknya oleh circle, menandakan circle umumnya tidak menghambat fokus belajar."
        )


    # Persepsi Motivasi & Motivasi Penyelesaian Tugas (kategorikal)
    # 7. Seberapa setuju Anda bahwa circle pertemanan dapat meningkatkan motivasi belajar Anda? (Persepsi Motivasi)
    # 9. Dari skala 1–5, seberapa besar circle pertemanan Anda memotivasi Anda untuk menyelesaikan tugas tepat waktu? (Motivasi Penyelesaian Tugas)

    col9, col10, col11 = st.columns(3)

    with col9:
        persepsi_count = filtered_df['Persepsi Motivasi Kategori'].value_counts().reset_index()
        persepsi_count.columns = ['Persepsi Motivasi', 'Jumlah']
        fig_persepsi = px.bar(
            persepsi_count,
            y='Persepsi Motivasi',
            x='Jumlah',
            orientation='h',
            title='Persepsi Motivasi Belajar dari Circle',
            color_discrete_sequence=custom_blues,
            color='Persepsi Motivasi'
        )
        fig_persepsi.update_layout(common_layout, showlegend=False, yaxis={'categoryorder':'total ascending'})
        fig_persepsi.update_yaxes(automargin=True)
        st.plotly_chart(fig_persepsi, use_container_width=True)
        
        # Insight persepsi motivasi fitur kategorikal
        persepsi_setuju_sangat_setuju = filtered_df['Persepsi Motivasi Kategori'].isin(['Setuju', 'Sangat Setuju']).mean() * 100

        if persepsi_setuju_sangat_setuju >= 50:
            persepsi_insight = "mayoritas responden memiliki persepsi positif terhadap motivasi belajar dari circle."
        else:
            persepsi_insight = "mayoritas responden kurang memiliki persepsi positif terhadap motivasi belajar dari circle."

        st.markdown(
            f"**Insight:** Sebanyak **{persepsi_setuju_sangat_setuju:.1f}%** yang memilih **Setuju** atau **Sangat Setuju**, menunjukkan bahwa {persepsi_insight}"
        )
    
    # Konsistensi dukungan belajar horizontal
    with col10:
        konsistensi_count = filtered_df['Konsistensi Dukungan Belajar Kategori'].value_counts().reset_index()
        konsistensi_count.columns = ['Konsistensi Dukungan', 'Jumlah']
        fig_konsistensi = px.bar(
            konsistensi_count,
            y='Konsistensi Dukungan',
            x='Jumlah',
            title='Konsistensi Dukungan Belajar dari Circle',
            orientation='h',
            color='Konsistensi Dukungan',
            color_discrete_sequence=custom_blues
        )
        fig_konsistensi.update_layout(common_layout, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_konsistensi, use_container_width=True)

        # Insight konsistensi dukungan belajar fitur kategorikal
        konsistensi_konsisten_sangat_konsisten = filtered_df['Konsistensi Dukungan Belajar Kategori'].isin(['Konsisten', 'Sangat Konsisten']).mean() * 100


        if konsistensi_konsisten_sangat_konsisten >= 50:
            konsistensi_insight = "mayoritas responden merasa mendapatkan dukungan belajar yang konsisten dari circle."
        else:
            konsistensi_insight = "mayoritas responden merasa kurang mendapatkan dukungan belajar yang konsisten dari circle."
        
        st.markdown(
            f"**Insight:** Sebanyak **{konsistensi_konsisten_sangat_konsisten:.1f}%** yang memilih **Konsisten** atau **Sangat Konsisten**, menunjukkan bahwa {konsistensi_insight}"
        )

    with col11:
        motivasi_count = filtered_df['Motivasi Penyelesaian Tugas Kategori'].value_counts().reset_index()
        motivasi_count.columns = ['Motivasi Penyelesaian Tugas', 'Jumlah']
        fig_motivasi = px.bar(
            motivasi_count,
            y='Motivasi Penyelesaian Tugas',
            x='Jumlah',
            title='Motivasi Penyelesaian Tugas dari Circle',
            orientation='h',
            color='Motivasi Penyelesaian Tugas',
            color_discrete_sequence=custom_blues
        )
        fig_motivasi.update_layout(common_layout, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_motivasi, use_container_width=True)

        # Insight motivasi penyelesaian tugas fitur kategorikal
        motivasi_termotivasi_sangat_termotivasi = filtered_df['Motivasi Penyelesaian Tugas Kategori'].isin(['Termotivasi', 'Sangat Termotivasi']).mean() * 100

        if motivasi_termotivasi_sangat_termotivasi >= 50:
            motivasi_insight = "mayoritas responden merasa termotivasi menyelesaikan tugas tepat waktu oleh circle."

        else:
            motivasi_insight = "mayoritas responden kurang merasa termotivasi menyelesaikan tugas tepat waktu oleh circle."

        st.markdown(
            f"**Insight:** Sebanyak **{motivasi_termotivasi_sangat_termotivasi:.1f}%** yang memilih **Termotivasi** atau **Sangat Termotivasi**, menunjukkan bahwa {motivasi_insight}"
        )

    

    st.markdown("---")


    # ---------------------------
    st.markdown("### 🔎 Highlight Cepat")
    top3_prodi = filtered_df['Program Studi'].value_counts().head(3)
    top3_str = ", ".join([f"{i+1}. {idx} ({cnt})" for i,(idx,cnt) in enumerate(top3_prodi.items())])

    st.markdown(
        f"- **Top 3 Program Studi** dengan responden terbanyak: {top3_str}.\n"
        f"- **{pct_small:.1f}%** responden memiliki circle kecil (≤5 orang), yang cenderung lebih intim dan mendukung interaksi mendalam.\n"
        f"- Mayoritas responden melaporkan tingkat dukungan circle sebagai **{top_support['Dukungan Circle']}**, menunjukkan peran positif circle dalam mendukung akademik.\n"
        f"- Sebanyak **{hi:.1f}%** responden tidak merasa terganggu akademiknya oleh circle, menandakan circle umumnya tidak menghambat fokus belajar.\n"
        f"- Sebanyak **{konsistensi_konsisten_sangat_konsisten:.1f}%** responden merasa mendapatkan dukungan belajar yang konsisten dari circle, menegaskan peran circle dalam menyediakan dukungan akademik yang stabil.\n"
        f"- Sebanyak **{persepsi_setuju_sangat_setuju:.1f}%** responden memiliki persepsi positif terhadap motivasi belajar dari circle, menunjukkan pengaruh sosial yang signifikan.\n"
        f"- Sebanyak **{motivasi_termotivasi_sangat_termotivasi:.1f}%** responden merasa termotivasi oleh circle, menegaskan peran circle dalam mendorong penyelesaian tugas tepat waktu."
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #9fb3c8; font-size: 13px;">
            🌐 Dashboard ini dikembangkan sebagai bagian dari analisis sosial akademik berbasis data oleh tim MEJIKUHIBINIU – 2025
        </div>
        """,
        unsafe_allow_html=True
    )    

with tab2:
    st.title("📈 Analisis Korelasi Antar Variabel")

    st.markdown("""
    Analisis korelasi digunakan untuk mengetahui **hubungan linear** antar variabel numerik 
    dalam dataset ini. Korelasi dapat menunjukkan arah (+ / −) dan kekuatan hubungan 
    (lemah, sedang, atau kuat).  
    """)
    st.markdown("---")
    # Ambil kolom numerik
    num_df = df.select_dtypes(include=['int64', 'float64'])

    # ==============================
    # 1️⃣ HEATMAP KORELASI PEARSON
    # ==============================
    st.subheader("1️⃣ Heatmap Korelasi Pearson")

    corr_matrix = num_df.corr(method='pearson')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="Blues", center=0, ax=ax, vmin=-1, vmax=1,
                cbar_kws={"shrink": .8, 'label': 'Korelasi (r)', 'orientation': 'vertical', 'ticks': [-1, -0.5, 0, 0.5, 1], 'pad':0.02, 'aspect':30, 'fraction':0.05})
    fig.patch.set_facecolor('#1e293b')  # Ubah warna background figure
    ax.set_facecolor('#1e293b')         # Ubah warna background axes
    # ubah warna semua teks dari judul, label, dan ticks menjadi putih
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')

    # ubah warna parameter korelasi bar kanan menjadi putih
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(colors='white')

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.title("Heatmap Korelasi Pearson Antar Variabel Numerik", pad=20)
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""
    🔹 **Interpretasi singkat:**  
    - Nilai mendekati **+1** → hubungan linear positif yang kuat.  
    - Nilai mendekati **−1** → hubungan linear negatif yang kuat.  
    - Nilai mendekati **0** → tidak ada hubungan linear yang kuat.  
    """)
    st.markdown("---")
    # ==============================
    # 2️⃣ INTERPRETASI OTOMATIS
    # ==============================
    st.subheader("2️⃣ Interpretasi Korelasi Terkuat")

    # Ambil korelasi terkuat (positif dan negatif) salah satu arah
    corr_pairs = corr_matrix.unstack()
    corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) != corr_pairs.index.get_level_values(1)]
    corr_pairs = corr_pairs.drop_duplicates().sort_values(ascending=False)
    top_pos_corr = corr_pairs[corr_pairs > 0].head(3)
    top_neg_corr = corr_pairs[corr_pairs < 0].tail(3)

    st.markdown("📈 **Korelasi Positif Terkuat:**")
    for (var1, var2), corr_value in top_pos_corr.items():
        st.markdown(f"- **{var1}** dan **{var2}**: r = {corr_value:.2f}")
    st.markdown("📉 **Korelasi Negatif Terkuat:**")

    # urut dari yang paling negatif
    top_neg_corr = top_neg_corr.sort_values()
    for (var1, var2), corr_value in top_neg_corr.items():
        st.markdown(f"- **{var1}** dan **{var2}**: r = {corr_value:.2f}")

    st.markdown("---")
    # 3. INSIGHT KHUSUS AUTOMATIS
    st.subheader("3️⃣ Highlight Insight")
    st.markdown(
        f"- Korelasi positif terkuat adalah antara **{top_pos_corr.index[0][0]}** dan **{top_pos_corr.index[0][1]}** (r = {top_pos_corr.iloc[0]:.2f}), menunjukkan bahwa peningkatan pada satu variabel cenderung diikuti oleh peningkatan pada variabel lainnya.\n"
        f"- Korelasi negatif terkuat adalah antara **{top_neg_corr.index[0][0]}** dan **{top_neg_corr.index[0][1]}** (r = {top_neg_corr.iloc[0]:.2f}), menunjukkan bahwa peningkatan pada satu variabel cenderung diikuti oleh penurunan pada variabel lainnya.\n"
        f"- Korelasi yang mendekati nol, seperti antara **{corr_pairs[corr_pairs.abs() < 0.1].index[0][0]}** dan **{corr_pairs[corr_pairs.abs() < 0.1].index[0][1]}** (r = {corr_pairs[corr_pairs.abs() < 0.1].iloc[0]:.2f}), menunjukkan tidak adanya hubungan linear yang signifikan antara kedua variabel tersebut."
    )
    

    st.markdown(
        """
        <div style="text-align: center; color: #9fb3c8; font-size: 13px;">
            🌐 Dashboard ini dikembangkan sebagai bagian dari analisis sosial akademik berbasis data oleh tim MEJIKUHIBINIU – 2025
        </div>
        """,
        unsafe_allow_html=True
    )

with tab3:
    st.title("⚔️ Analisis Perbandingan Fasilkom vs Non-Fasilkom")

    st.markdown("""
    Bagian ini membandingkan **perbedaan rata-rata** variabel numerik antara dua kelompok: 
    mahasiswa **Fasilkom** dan **Non-Fasilkom**.  
    """)
    st.markdown("---")

    # ==============================
    # 1️⃣ T-TEST INDEPENDEN
    # ==============================
    st.subheader("1️⃣ Uji t-test Independen")

    df = filtered_df
    df['Kelompok'] = np.where(df['Fakultas'] == 'FASILKOM', 'Fasilkom', 'Non-Fasilkom')
    kelompok1 = df[df['Kelompok'] == 'Fasilkom']
    kelompok2 = df[df['Kelompok'] == 'Non-Fasilkom']
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    ttest_results = []
    for col in num_cols:
        t_stat, p_val = stats.ttest_ind(kelompok1[col], kelompok2[col], nan_policy='omit')
        mean1 = kelompok1[col].mean()
        mean2 = kelompok2[col].mean()
        ttest_results.append((col, mean1, mean2, t_stat, p_val))
    ttest_df = pd.DataFrame(ttest_results, columns=['Variabel', 'Mean Fasilkom', 'Mean Non-Fasilkom', 't-statistic', 'p-value'])
    ttest_df['Signifikan (α=0.05)'] = ttest_df['p-value'] < 0.05
    st.dataframe(ttest_df)
    # Interpretasi singkat kenapa terdapat perbedaan yang signifikan apa kriterianya
    st.markdown("""
    **Kriteria Keputusan Uji t-test Independen:**
    - p-value < 0.05 → perbedaan rata-rata signifikan secara statistik.
    - p-value ≥ 0.05 → tidak ada perbedaan rata-rata yang signifikan.
    """)
    st.markdown("---")

    # ==============================
    # 2️⃣ INTERPRETASI OTOMATIS
    # ==============================
    st.subheader("2️⃣ Interpretasi Hasil Uji t-test")
    signifikan_df = ttest_df[ttest_df['Signifikan (α=0.05)']]
    if signifikan_df.empty:
        st.markdown("Tidak ada perbedaan rata-rata yang signifikan antara Fasilkom dan Non-Fasilkom pada variabel numerik.")
    else:   
        for _, row in signifikan_df.iterrows():
            var = row['Variabel']
            mean1 = row['Mean Fasilkom']
            mean2 = row['Mean Non-Fasilkom']
            p_val = row['p-value']
            if mean1 > mean2:
                st.markdown(f"- Terdapat perbedaan rata-rata **{var}** lebih tinggi pada **Fasilkom** ({mean1:.2f}) dibanding **Non-Fasilkom** ({mean2:.2f}), dengan p-value = {p_val:.4f}.")
            else:
                st.markdown(f"- Terdapat perbedaan rata-rata **{var}** lebih tinggi pada **Non-Fasilkom** ({mean2:.2f}) dibanding **Fasilkom** ({mean1:.2f}), dengan p-value = {p_val:.4f}.")
    
    st.markdown("- Ini bisa menunjukkan perbedaan karakteristik akademik atau sosial antara mahasiswa Fasilkom dan Non-Fasilkom, bahwasanya mahasiswa Fasilkom cenderung kurang untuk bertemu dan belajar bersama sesama anggota circle dibanding mahasiswa Non-Fasilkom dikarenakan kebanyakan tugasnya mungkin bersifat individu atau online (ngoding).")
    st.markdown(f"- Tidak ada perbedaan signifikan pada variabel lain seperti {', '.join(set(num_cols) - set(signifikan_df['Variabel'].tolist()))}, menunjukkan bahwa kedua kelompok memiliki karakteristik serupa pada aspek-aspek tersebut.")
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align: center; color: #9fb3c8; font-size: 13px;">
            🌐 Dashboard ini dikembangkan sebagai bagian dari analisis sosial akademik berbasis data oleh tim MEJIKUHIBINIU – 2025
        </div>
        """,
        unsafe_allow_html=True
    )

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# UJI F DAN UJI t
with tab4:
    st.title("🧮 Analisis Regresi Linear Berganda")

    st.markdown("""
    Bagian ini melakukan **regresi linear berganda** untuk memodelkan hubungan antara 
    variabel dependen (target) dan beberapa variabel independen (prediktor).  
    """)
    st.markdown("---")

    # ==============================
    # 1️⃣ PEMODELAN REGRESI
    # ==============================
    st.subheader("1️⃣ Pemodelan Regresi Linear Berganda")

    df = filtered_df

    # Pilih variabel dependen dan independen
    target_var = 'Motivasi Penyelesaian Tugas'
    feature_vars = [
        'Jumlah Anggota Circle',
        'Frekuensi Bertemu Seminggu',
        'Frekuensi Belajar Bersama Seminggu',
        'Konsistensi Dukungan Belajar',
        'Durasi Belajar Sehari',
        'Persepsi Motivasi'
    ]

    X = df[feature_vars]
    y = df[target_var]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    coefficients = pd.DataFrame({
        'Variabel': feature_vars,
        'Koefisien': model.coef_
    })
    # UBAH VARIABEL INDEPENDEN MENJADI X1, X2, dst UNTUK PERSAMAAN REGRESI
    coefficients['Variabel'] = ['X' + str(i+1) for i in range(len(feature_vars))]
    feature_vars = coefficients['Variabel'].tolist()

    # DataFrame untuk nama variabel Y dan X1, X2, ...
    coefficients_display = pd.DataFrame({
        'Nama Asli': [target_var] + [
            'Jumlah Anggota Circle',
            'Frekuensi Bertemu Seminggu',
            'Frekuensi Belajar Bersama Seminggu',
            'Konsistensi Dukungan Belajar',
            'Durasi Belajar Sehari',
            'Persepsi Motivasi'
        ],
        'Variabel': ['Y'] + feature_vars
    })
    st.markdown("**Daftar Variabel:**")
    st.dataframe(coefficients_display)

    # PERSAMAAN REGRESI
    intercept = model.intercept_
    equation_terms = [f"{coef:.4f}*{var}" for coef, var in zip(model.coef_, feature_vars)]
    equation = " + ".join(equation_terms)
    st.markdown("**Persamaan Regresi Linear Berganda:**")
    st.latex(f"Y = {intercept:.4f} + {equation}")
    st.markdown("---")

    # ==============================
    # 2️⃣ UJI F
    # ==============================
    st.subheader("2️⃣ Uji F untuk Signifikansi Model Regresi")
    # TABEL ANOVA
    st.markdown("**Tabel ANOVA:**")
    anova_table = pd.DataFrame({
        'Sum of Squares': [np.sum((y_pred - np.mean(y))**2), np.sum((y - y_pred)**2), np.sum((y - np.mean(y))**2)],
        'df': [len(feature_vars), len(y) - len(feature_vars) - 1, len(y) - 1],
        'Mean Square': [np.sum((y_pred - np.mean(y))**2)/len(feature_vars), np.sum((y - y_pred)**2)/(len(y) - len(feature_vars) - 1), np.sum((y - np.mean(y))**2)/(len(y) - 1)],
        'F': [ (np.sum((y_pred - np.mean(y))**2)/len(feature_vars)) / (np.sum((y - y_pred)**2)/(len(y) - len(feature_vars) - 1)), np.nan, np.nan],
        'p-value': [1 - stats.f.cdf((np.sum((y_pred -   np.mean(y))**2)/len(feature_vars)) / (np.sum((y - y_pred)**2)/(len(y) - len(feature_vars) - 1)), len(feature_vars), len(y) - len(feature_vars) - 1), np.nan, np.nan]
    }, index=['Regression', 'Error', 'Total'])
    st.dataframe(anova_table)

    st.markdown("**Kriteria Keputusan Uji F:**")
    st.markdown("- Jika F statistic > F table → Tolak H0 (model regresi signifikan secara statistik).")
    st.markdown("- Jika F statistic ≤ F table → Gagal tolak H0 (model regresi tidak signifikan secara statistik).")

    # UJI F dengan F table
    alpha = 0.05
    f_table = stats.f.ppf(1 - alpha, len(feature_vars), len(y) - len(feature_vars) - 1)
    f_stat = anova_table.loc['Regression', 'F']
    st.markdown("**Hasil Uji F:**")
    st.markdown(f"- **F statistic** = **{f_stat:.4f}**")
    st.markdown(f"- **F table** (α = {alpha}, df1 = {len(feature_vars)}, df2 = {len(y) - len(feature_vars) - 1}) = **{f_table:.4f}**")



    st.markdown("**Kesimpulan Uji F:**")

    if f_stat > f_table:
        st.markdown("-  **F statistic > F table** → **Tolak H0** (model regresi signifikan secara statistik) sehingga dapat kita lanjutkan ke **Uji t** untuk melihat variabel mana yang signifikan secara individual.")
    else:
        st.markdown("-  **F statistic ≤ F table** → **Gagal tolak H0** (model regresi tidak signifikan secara statistik) sehingga tidak perlu melanjutkan ke **Uji t** karena modelnya tidak signifikan.")

    st.markdown("---")
    # UJI t untuk setiap variabel X1, X2, ...
    if f_stat > f_table:
        st.subheader("3️⃣ Uji t untuk Signifikansi Setiap Variabel Independen")
        st.markdown("**Hasil Uji t untuk Setiap Variabel Independen:**")
        ttest_results = []
        for i, var in enumerate(feature_vars):
            se = np.sqrt(mse / np.sum((X.iloc[:, i] - X.iloc[:, i].mean())**2))
            t_stat = model.coef_[i] / se
            p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=len(y) - len(feature_vars) - 1))
            ttest_results.append((var, model.coef_[i], t_stat, p_val))
        ttest_df = pd.DataFrame(ttest_results, columns=['Variabel', 'Koefisien', 't-statistic', 'p-value'])
        ttest_df['Signifikan (α=0.05)'] = ttest_df['p-value'] < 0.05
        st.dataframe(ttest_df)

        st.markdown("**Kriteria Keputusan Uji t:**")
        st.markdown("- |t-statistic| > t table → Tolak H0 (variabel signifikan secara statistik).")
        st.markdown("- |t-statistic| ≤ t table → Gagal tolak H0 (variabel tidak signifikan secara statistik).")
        t_table = stats.t.ppf(1 - alpha/2, df=len(y) - len(feature_vars) - 1)

        st.markdown("**Hasil Uji t:**")
        st.markdown(f"- **t table** (α = {alpha}, df = {len(y) - len(feature_vars) - 1}) = **{t_table:.4f}**")
        for _, row in ttest_df.iterrows():
            var = row['Variabel']
            t_stat = row['t-statistic']
            p_val = row['p-value']
            if abs(t_stat) > t_table:
                st.markdown(f"- Variabel **{var}**: |t-statistic| = **{abs(t_stat):.4f}** > t table → **Tolak H0** (variabel signifikan secara statistik, p-value = {p_val:.4f}).")
            else:
                st.markdown(f"- Variabel **{var}**: |t-statistic| = **{abs(t_stat):.4f}** ≤ t table → **Gagal tolak H0** (variabel tidak signifikan secara statistik, p-value = {p_val:.4f}).")

        st.markdown("**Kesimpulan Uji t:**")
        signifikan_df = ttest_df[ttest_df['Signifikan (α=0.05)']]
        if signifikan_df.empty:
            st.markdown("Tidak ada variabel independen yang signifikan secara statistik dalam memprediksi variabel dependen.")
        else:   
            for _, row in signifikan_df.iterrows():
                var = row['Variabel']
                coef = row['Koefisien']
                p_val = row['p-value']
                nama_asli = coefficients_display[coefficients_display['Variabel'] == var]['Nama Asli'].values[0]
                if coef > 0:
                    st.markdown(f"- Variabel **{var}** yaitu **{nama_asli}** memiliki koefisien positif ({coef:.4f}) dan signifikan (p-value = {p_val:.4f}), menunjukkan bahwa peningkatan pada variabel ini cenderung diikuti oleh peningkatan pada variabel dependen.")
                else:
                    st.markdown(f"- Variabel **{var}** yaitu **{nama_asli}** memiliki koefisien negatif ({coef:.4f}) dan signifikan (p-value = {p_val:.4f}), menunjukkan bahwa peningkatan pada variabel ini cenderung diikuti oleh penurunan pada variabel dependen.")
        st.markdown(f"- Variabel yang tidak signifikan secara statistik tidak memberikan kontribusi yang berarti dalam memprediksi variabel dependen seperti pada variabel **{', '.join(set(feature_vars) - set(signifikan_df['Variabel'].tolist()))}** yaitu **{', '.join([coefficients_display[coefficients_display['Variabel'] == var]['Nama Asli'].values[0] for var in set(feature_vars) - set(signifikan_df['Variabel'].tolist())])}**.")
    else:
        st.markdown("Karena model regresi tidak signifikan secara statistik berdasarkan Uji F, maka Uji t untuk setiap variabel independen tidak dilakukan.")

    st.markdown("---")
    # Kesimpulan Akhir Regresi Linear Berganda
    st.subheader("4️⃣ Kesimpulan Akhir")
    st.markdown("Persamaan model regesii linear berganda yang diperoleh yaitu sebagai berikut:")
    st.latex(f"Y = {intercept:.4f} + {equation}")
    st.markdown(f"Dimana Y adalah **{target_var}**, dan X1, X2, ..., X{len(feature_vars)} adalah variabel independen yang telah dijelaskan sebelumnya.")
    if f_stat > f_table:
        st.markdown(f"- Model regresi linear berganda signifikan secara statistik (F statistic = {f_stat:.4f} > F table = {f_table:.4f}), dengan R² = {r2:.4f}, menunjukkan bahwa sekitar {r2*100:.2f}% variasi dalam **{target_var}** dapat dijelaskan oleh variabel independen yang dipilih.")
        if not signifikan_df.empty:
            # nama asli variabel signifikan
            st.markdown(f"- Variabel independen yang signifikan secara statistik dalam memprediksi **{target_var}** adalah: {', '.join(signifikan_df['Variabel'].tolist())} yaitu {', '.join([coefficients_display[coefficients_display['Variabel'] == var]['Nama Asli'].values[0] for var in signifikan_df['Variabel'].tolist()])}.")
            st.markdown("- Variabel-variabel ini memberikan kontribusi yang berarti dalam memprediksi variabel dependen dan dapat menjadi fokus untuk intervensi atau strategi peningkatan motivasi penyelesaian tugas.")
        else:
            st.markdown(f"- Tidak ada variabel independen yang signifikan secara statistik dalam memprediksi **{target_var}**, menunjukkan bahwa variabel-variabel yang dipilih mungkin tidak relevan atau ada faktor lain yang lebih berpengaruh.")


    st.markdown("---")
    st.markdown(
            """
            <div style="text-align: center; color: #9fb3c8; font-size: 13px;">
                🌐 Dashboard ini dikembangkan sebagai bagian dari analisis sosial akademik berbasis data oleh tim MEJIKUHIBINIU – 2025
            </div>
            """,
            unsafe_allow_html=True

    )



