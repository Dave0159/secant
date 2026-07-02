# 📈 Secant Method Calculator

Aplikasi interaktif berbasis **Streamlit** untuk mencari akar persamaan nonlinier menggunakan **Metode Secant (Secant Method)**.

Aplikasi ini memungkinkan pengguna memasukkan fungsi matematika secara bebas, melihat grafik fungsi, menentukan tebakan awal, kemudian menjalankan iterasi metode secant lengkap dengan visualisasi proses konvergensinya.

Accsess here
https://secant.streamlit.app/
---

## ✨ Fitur

- 📌 Input persamaan matematika secara bebas
- 📊 Grafik fungsi interaktif menggunakan Plotly
- 🎯 Menentukan nilai awal `x₀` dan `x₁`
- ⚙️ Mengatur toleransi error dan maksimum iterasi
- 📋 Menampilkan tabel seluruh proses iterasi
- 📉 Visualisasi titik-titik iterasi menuju akar
- ✅ Status konvergen atau tidak konvergen
- 🌙 Mendukung Light Mode dan Dark Mode
- 🧮 Mendukung berbagai fungsi matematika SymPy

---
# 📚 Metode Secant

Metode Secant merupakan metode numerik untuk mencari akar persamaan

\[
f(x)=0
\]

dengan menggunakan dua tebakan awal tanpa memerlukan turunan fungsi.

Rumus iterasi:

\[
x_{i+1}=x_i-\frac{f(x_i)(x_i-x_{i-1})}{f(x_i)-f(x_{i-1})}
\]

Metode ini biasanya memiliki konvergensi yang lebih cepat dibanding metode Regula Falsi, namun tidak selalu menjamin konvergensi.

---

# 🚀 Cara Menjalankan

## 1. Clone Repository

```bash
git clone https://github.com/Dave0159/secant.git

cd secant
```

---

## 2. Install Dependencies

Disarankan menggunakan Virtual Environment.

```bash
pip install -r requirements.txt
```

Apabila belum tersedia `requirements.txt`, install package berikut:

```bash
pip install streamlit
pip install numpy
pip install pandas
pip install plotly
pip install sympy
```

---

## 3. Jalankan Program

```bash
streamlit run app.py
```

Setelah itu buka browser pada

```
http://localhost:8501
```

---

# 📝 Cara Menggunakan

### 1. Masukkan Persamaan

Contoh:

```
x^3 - x - 2
```

atau

```
sin(x)-x/2
```

atau

```
exp(x)-3*x
```

Program mendukung:

- `+`
- `-`
- `*`
- `/`
- `^`
- `**`
- `sqrt()`
- `sin()`
- `cos()`
- `tan()`
- `log()`
- `ln()`
- `exp()`
- `abs()`

---

### 2. Atur Rentang Grafik

Masukkan:

- Batas bawah sumbu-x
- Batas atas sumbu-x

Grafik akan membantu memperkirakan letak akar.

---

### 3. Tentukan Tebakan Awal

Masukkan:

- x₀
- x₁

Usahakan kedua nilai berada dekat dengan akar agar proses konvergen lebih cepat.

---

### 4. Atur Parameter

Isi:

- Toleransi error

contoh

```
0.000001
```

dan

- Maksimum Iterasi

misalnya

```
50
```

---

### 5. Jalankan

Tekan tombol

```
Jalankan Metode Secant
```

---

# 📊 Output Program

Program akan menampilkan:

- Jumlah iterasi
- Nilai akar yang diperoleh
- Nilai fungsi pada akar
- Status konvergen
- Tabel seluruh iterasi
- Grafik konvergensi metode secant

---

# 📌 Contoh Persamaan

### Persamaan Polinomial

```
x^3-x-2
```

---

### Persamaan Trigonometri

```
sin(x)-x/2
```

---

### Persamaan Eksponensial

```
exp(x)-3*x
```

---

### Persamaan Logaritma

```
log(x)-1
```

---

# 🛠 Teknologi

- Python
- Streamlit
- SymPy
- NumPy
- Pandas
- Plotly

---

# 📂 Struktur Project

```
secant/
│
├── app.py
├── requirements.txt
├── README.md
└──  image.png
```

---

# 📖 Referensi

- Burden & Faires - Numerical Analysis
- Chapra - Applied Numerical Methods
- Dokumentasi Streamlit
- Dokumentasi SymPy

---

# 👨‍💻 Author

**Dave0159**

GitHub:
https://github.com/Dave0159

---

# ⭐ Dukungan

Apabila project ini bermanfaat, jangan lupa memberikan ⭐ pada repository GitHub ini agar dapat membantu pengembangan selanjutnya.
