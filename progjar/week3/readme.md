# Pattern Maze Solver

Script ini digunakan untuk menyelesaikan challenge **Pattern Maze** dengan cara melakukan traversal otomatis hingga menemukan flag.

---

## Cara Menjalankan

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4
```

### 2. Jalankan Program

```bash
python3 maze.py
```

Program akan:
- Menelusuri semua kemungkinan path pada maze
- Mencari halaman dengan marker <<<YOU FOUND ME>>>
- Mengambil flag secara otomatis

### 3.Submit Flag

Setelah mendapatkan flag, submit menggunakan:

```bash
curl -X POST https://progjar.web.id/submit \
  -H "Content-Type: application/json" \
  -d '{"nrp":"NRP_KAMU","flag":"FLAG{...}"}'
```

### Catatan Penting

1. Redirect

Website menggunakan redirect dari HTTP ke HTTPS: `HTTP/1.1 308 Permanent Redirect`

Untuk mengatasinya, gunakan flag -L pada curl:
`curl -L -H "NRP: 5025241234" http://progjar.web.id/maze`

2. Penjelasan Perintah curl

`curl -v -H "NRP: 5025241234" http://progjar.web.id/maze`
`-H` → Menambahkan header (digunakan untuk mengirim NRP)
`-v` → Verbose mode (menampilkan detail request & response)
`-i` → Menampilkan header response
`-L` → Follow redirect otomatis

### Penjelsan Kode

1. Setup

```bash
NRP = "5025241xxx"
BASE = "https://progjar.web.id"
START = "/maze"
```

Untuk mengatur alamat start dan nrp.

2. Session Request

```python
sess = requests.Session()
sess.headers.update({"NRP": NRP})
```

Semua request akan otomatis membawa header: `NRP: 5025241031`

3. Prevent Loop

```python
visited = set()
```

Digunakan untuk menyimpan path yang sudah dikunjungi agar tidak terjadi infinite loop.

4. Fungsi DFS (Traversal)

```python
def dfs(path):
```

Menggunakan algoritma Depth First Search (DFS) untuk menjelajahi semua kemungkinan jalur dalam maze.

**Flow:**

- Ambil halaman
- Ambil semua link `/maze/...`
- Masuk ke setiap cabang
- Berhenti jika flag ditemukan

5. Extract Informasi dari Response

```python
html, links = extract_everything(resp)
```

Fungsi ini:

- Mengambil HTML
- Mencari header penting
- Mencari komentar HTML
- Mengambil semua link berikutnya

6. Deteksi Halaman Flag

```python
if "<<<YOU FOUND ME>>>" in html or "FLAG{" in html:
```

Jika ditemukan:
- Marker khusus
- atau format flag

7. Extract Flag

```python
m = re.search(r'FLAG\{[^}]+\}', html)
```

Menggunakan regex untuk mengambil flag dari HTML.

8. Traversal Rekursif

```python
for link in links:
    res = dfs(link)
```

Menelusuri semua cabang secara rekursif sampai menemukan flag.

### 🔍 Cara Kerja Singkat

```
/maze
  ↓
lvl1
  ↓
lvl2
  ↓
lvl3
  ↓
lvl4
  ↓
lvl5
  ↓
lvl6
  ↓
FLAG
```

Script akan mencoba semua kemungkinan path sampai menemukan jalur yang benar.

### Catatan

- Maze bersifat deterministic berdasarkan NRP
- Tanpa header NRP, hasil akan berbeda atau tidak valid
- Brute force masih aman karena depth kecil (6 level)
