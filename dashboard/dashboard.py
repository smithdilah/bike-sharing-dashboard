import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
df_hour = pd.read_csv("dashboard/main_data.csv")
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])  # Konversi ke datetime

# Mapping Kategori Cuaca
weather_mapping = {
    1: "Cerah/Berawan",
    2: "Mendung",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
}
df_hour["weathersit"] = df_hour["weathersit"].map(weather_mapping)

# Fungsi clustering waktu
def cluster_time(hour):
    if 6 <= hour < 10:
        return "Pagi (Rush Hour)"
    elif 10 <= hour < 16:
        return "Siang"
    elif 16 <= hour < 20:
        return "Sore (Rush Hour)"
    else:
        return "Malam"

df_hour["time_cluster"] = df_hour["hr"].apply(cluster_time)

# Streamlit App
st.title("🚲 Dashboard Bike Sharing")
st.write("Analisis interaktif penggunaan sepeda berdasarkan waktu dan cuaca.")

# Sidebar Filter
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", df_hour["dteday"].min())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", df_hour["dteday"].max())
filtered_df = df_hour[(df_hour["dteday"] >= pd.to_datetime(start_date)) & (df_hour["dteday"] <= pd.to_datetime(end_date))]

# Warna Custom untuk Visualisasi
high_usage_color = "#1D3557"  # Warna untuk waktu dengan penggunaan tinggi (Pagi & Sore)
medium_usage_color = "#A8DADC"  # Warna untuk penggunaan sedang (Siang)
low_usage_color = "#F1FAEE"  # Warna untuk penggunaan rendah (Malam)

# Plot 1: Pola Penggunaan Sepeda berdasarkan Jam
st.subheader("📊 Pola Penggunaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="hr", y="cnt", color=high_usage_color, linewidth=2, ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Plot 2: Jumlah Pengguna Berdasarkan Cluster Waktu
st.subheader("⏳ Jumlah Pengguna Berdasarkan Cluster Waktu")
fig, ax = plt.subplots(figsize=(8, 5))
cluster_palette = {
    "Pagi (Rush Hour)": high_usage_color,
    "Sore (Rush Hour)": high_usage_color,
    "Siang": medium_usage_color,
    "Malam": low_usage_color,
}
sns.barplot(data=filtered_df, x="time_cluster", y="cnt", estimator="mean", palette=cluster_palette, ax=ax)
ax.set_xlabel("Cluster Waktu")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Plot 3: Pengaruh Cuaca terhadap Penggunaan Sepeda
st.subheader("🌦️ Pengaruh Cuaca terhadap Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weathersit", y="cnt", data=filtered_df, estimator="mean", palette=[high_usage_color, medium_usage_color, "#E63946", low_usage_color], ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Insight
st.write("📌 **Insight:**")
st.write("- Penggunaan sepeda paling tinggi saat **Rush Hour** (pagi & sore).")
st.write("- **Cuaca cerah** meningkatkan jumlah pengguna secara signifikan.")
st.write("- **Hujan lebat** mengurangi jumlah pengguna drastis.")
st.write("- Memilih rentang tanggal yang berbeda akan menunjukkan pola yang berbeda juga.")
