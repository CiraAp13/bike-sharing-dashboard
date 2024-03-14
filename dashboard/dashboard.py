# Mengimpor library 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya plot Seaborn menjadi 'dark'
sns.set(style='dark')

# Membaca file CSV dengan nama "all.csv" dan menyimpannya dalam dataframe all_df
# all_df = pd.read_csv("dashboard/all.csv")
all_df = pd.read_csv("all.csv")
all_df.head()

# Fungsi untuk menghitung total penyewaan sepeda per jam dari dataframe utama
def create_total_rent_per_hour(main_df) :
    return main_df.groupby('hr')['count'].sum().reset_index()

# Fungsi untuk menghitung penggunaan sepeda berdasarkan musim dari dataframe utama
def create_seasonal_usage(main_df) :
    return main_df.groupby('season')[['registered', 'casual']].sum().reset_index()

# Fungsi untuk menghitung rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca dari dataframe utama
def create_weather_con(main_df) :
    return main_df.groupby('weather_cond')['count'].mean().reset_index()


# Menentukan rentang tanggal minimum dan maksimum dari dataframe
min_date = pd.to_datetime(all_df['dateday']).dt.date.min()
max_date = pd.to_datetime(all_df['dateday']).dt.date.max()

# Menampilkan widget tanggal pada sidebar Streamlit untuk memilih rentang waktu
with st.sidebar:
    # st.image('dashboard/bicycle.png')
    st.image('bicycle.png')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter dataframe utama berdasarkan rentang waktu yang dipilih
main_df = all_df[(all_df['dateday'] >= str(start_date)) & 
                 (all_df['dateday'] <= str(end_date))]

# Menghitung rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca dari dataframe utama yang diperbarui
weather_con_df = create_weather_con(main_df)

# Menghitung penggunaan sepeda berdasarkan musim dari dataframe utama yang diperbarui
seasonal_usage_df = create_seasonal_usage(main_df)

# Menghitung total penyewaan sepeda per jam dari dataframe utama yang diperbarui
total_rent_per_hour_df = create_total_rent_per_hour(main_df)


# Pembuatan Dashboard

# Menambahkan header
st.header(':bike: Bike-Sharing-Dashboard :bike:')

st.subheader('Distribusi User')

# Menampilkan metrik tentang total pengguna, pengguna terdaftar, dan pengguna tidak terdaftar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Users", value=main_df['count'].sum())

with col2:
    st.metric("Registered Users", value=main_df['registered'].sum())

with col3:
    st.metric("Casual Users", value=main_df['casual'].sum())

# Menampilkan subjudul tentang total penyewaan sepeda berdasarkan pembagian jam
st.subheader('Total Penyewaan Sepeda Berdasarkan Pembagian Jam')

# Menentukan rentang jam menggunakan slider dari nilai 0 hingga 23, defaultnya adalah dari 0 hingga 23
values = st.slider('Rentang Jam :', 0, 23, (0, 23))
start_hour, end_hour = values

# Membuat objek gambar dengan ukuran 16x8
fig = plt.figure(figsize=(16, 8))

# Membuat plot garis menggunakan Seaborn untuk menampilkan total penyewaan sepeda per jam dalam rentang waktu yang ditentukan
ax = sns.lineplot(data=total_rent_per_hour_df[(total_rent_per_hour_df['hr'] >= start_hour) & (total_rent_per_hour_df['hr'] <= end_hour)], x="hr", y="count", color='orange', errorbar=None, marker="o")

# Menambahkan label sumbu x dan y, judul plot, serta grid
plt.xlabel("Jam")
plt.ylabel("Total Penyewaan Sepeda")
plt.title("Total Penyewaan Sepeda per Jam")
plt.grid()

# Menampilkan plot
plt.show()

# Menampilkan plot menggunakan st.pyplot() dari Streamlit
st.pyplot(fig)

# Menambahkan Penjelasan
st.write('Berdasarkan grafik tersebut, terdapat dua waktu puncak dalam jumlah penyewaan sepeda, yaitu pada jam 8 pagi dan jam 5 sore. Penurunan signifikan dalam jumlah penyewaan sepeda pada jam 8 pagi menunjukkan bahwa sebagian besar orang menggunakan sepeda sebagai sarana transportasi untuk pergi ke tempat kerja atau sekolah. Sementara itu, peningkatan jumlah penyewaan sepeda pada jam 5 sore menunjukkan bahwa sepeda juga banyak digunakan sebagai sarana transportasi untuk pulang dari tempat kerja atau sekolah. Pola ini menunjukkan bahwa ada tren penurunan penggunaan sepeda sepanjang pagi dan siang hari setelah mencapai puncak pada jam 8 pagi, kemungkinan karena orang-orang sudah mencapai tujuan mereka dan tidak lagi membutuhkan sepeda. Terakhir, jumlah penyewaan sepeda terendah terjadi pada jam 4 pagi, menandakan bahwa waktu ini adalah periode paling sepi dalam penggunaan layanan penyewaan sepeda. Dengan demikian, grafik ini memberikan wawasan yang penting bagi penyedia layanan sepeda untuk merencanakan operasional mereka, seperti menyiapkan lebih banyak sepeda pada jam-jam sibuk dan melakukan pemeliharaan pada jam-jam sepi.')

# Menampilkan subjudul untuk grafik berikutnya
st.subheader('Total Penyewaan Sepeda Berdasarkan Pembagian Musim')

# Membuat objek gambar dengan ukuran 10x6 untuk grafik berikutnya
fig = plt.figure(figsize=(10, 6))

# Membuat barplot horizontal untuk menampilkan total penyewaan sepeda berdasarkan musim
plt.barh(
    seasonal_usage_df['season'],
    seasonal_usage_df['registered'],
    label='Registered',
    color='tab:red'
)

plt.barh(
    seasonal_usage_df['season'],
    seasonal_usage_df['casual'],
    label='Casual',
    color='tab:orange'
)

plt.ylabel('Musim')  # Menjadikan musim sebagai label sumbu y
plt.xlabel(None)
plt.title('Total of Bike rentals Based on Season')
plt.gca().invert_yaxis()  # Membalik urutan sumbu y agar musim terurut dari atas ke bawah
plt.legend()
plt.show()

# Menampilkan plot menggunakan st.pyplot() dari Streamlit
st.pyplot(fig)

# Menambahkan Penjelasan
st.write('Dari grafik yang tersedia, tampak bahwa musim yang paling diminati untuk penyewaan sepeda adalah musim gugur. Baik pengguna terdaftar maupun pengguna kasual menunjukkan minat yang tinggi, dengan jumlah total penyewaan sepeda pada musim gugur lebih tinggi dibandingkan dengan musim lainnya. Lebih spesifik lagi, jumlah penyewaan sepeda mencapai puncaknya selama musim gugur, di mana baik pengguna terdaftar maupun pengguna kasual sama-sama menyewa sepeda dalam jumlah yang besar. Sedangkan di musim semi dan musim panas, jumlah penyewaan sepeda juga cukup tinggi, meskipun tidak sebanyak di musim gugur. Sementara itu, musim dingin menunjukkan jumlah penyewaan sepeda yang paling rendah, mungkin karena cuaca yang dingin membuat orang kurang cenderung untuk bersepeda. Dengan melihat grafik pula dapat kita lihat bahwa terdapat kecenderungan bahwa pengguna terdaftar menyewa sepeda lebih banyak dibandingkan pengguna kasual di setiap musim. Hal ini bisa saja menunjukkan bahwa pengguna terdaftar lebih sering menggunakan sepeda sebagai sarana transportasi sehari-hari, sementara pengguna kasual lebih cenderung menyewa sepeda untuk kegiatan rekreasi atau pariwisata, yang mungkin saja dipengaruhi oleh musim.')

# Menampilkan subjudul untuk grafik berikutnya
st.subheader('Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca')

# Membuat objek gambar dengan ukuran 10x6 untuk grafik
fig = plt.figure(figsize=(10, 6))

# Menggunakan Seaborn untuk membuat barplot yang menunjukkan rata-rata total penyewaan sepeda berdasarkan kondisi cuaca
sns.barplot(
    x=weather_con_df['weather_cond'],  # Menjadikan kondisi cuaca sebagai data untuk sumbu x
    y=weather_con_df['count'],  # Menjadikan rata-rata total penyewaan sepeda sebagai data untuk sumbu y
    data=all_df  # Menggunakan data dari dataframe all_df
)

# Menambahkan judul pada plot
plt.title('Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca')

# Menghapus label sumbu x
plt.xlabel('')

# Menambahkan label sumbu y sebagai "Rata-rata Total Penyewaan Sepeda"
plt.ylabel('Rata-rata Total Penyewaan Sepeda')

# Menampilkan plot
plt.show()

# Menampilkan plot menggunakan st.pyplot() dari Streamlit
st.pyplot(fig)


# Menambahkan Penjelasan
st.write('Ya, faktor cuaca memang memiliki pengaruh yang signifikan pada jumlah pengguna sepeda, seperti yang terlihat dari grafik. Terjadi peningkatan jumlah penyewaan sepeda saat cuaca cerah hingga berawan sedikit, menandakan bahwa kondisi cuaca yang baik mendorong lebih banyak orang untuk bersepeda. Di sisi lain, pada kondisi cuaca yang buruk seperti hujan lebat, salju, dan kabut, jumlah penyewaan sepeda mencapai titik terendah. Hal ini menunjukkan bahwa kondisi cuaca yang tidak mendukung dapat menghalangi orang untuk bersepeda.')