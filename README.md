# VCB DigiBank UNOFFICIAL API 🚀

## Giới thiệu 📢

Đây là project tự động hóa đăng nhập và lấy lịch sử giao dịch tài khoản Vietcombank (VCB DigiBank) thông qua API web. Dự án sử dụng Python để mô phỏng quá trình đăng nhập, giải captcha, mã hóa/giải mã dữ liệu và lấy thông tin giao dịch. Ngoài ra, project còn cung cấp giao diện web đơn giản để lấy BrowserID (Fingerprint) phục vụ cho quá trình đăng nhập.

## Tính năng ✨

- 🔐 Tự động đăng nhập tài khoản VCB DigiBank bằng username, password và BrowserID.
- 🤖 Tự động giải captcha bằng API (Dùng của mình hoặc tự build theo folder model).
- 🔒 Mã hóa/giải mã dữ liệu theo chuẩn của VCB.
- 📊 Lấy toàn bộ lịch sử giao dịch trong khoảng thời gian tùy chọn.
- 🌐 Hỗ trợ proxy và tùy chỉnh session.
- 🖥️ Giao diện web lấy BrowserID (Fingerprint) dễ sử dụng.

## Cấu trúc thư mục 📁

```
VCB/
├── main.py
├── utils/
│   ├── _algorithm.py
│   ├── captcha_solving.py
│   └── __init__.py
├── config/
│   └── user.json
├── broserid/
│   ├── index.html
│   ├── css/
│   │   └── fingerprint.css
│   └── js/
│       └── fingerprint.js
├── model/
│   ├── app.py
│   ├── captcha_model.h5
│   ├── example.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Hướng dẫn sử dụng 🛠️

### 1. Cài đặt thư viện

Cài đặt các thư viện cần thiết (yêu cầu Python 3.8+):

```sh
pip install -r requirements.txt
```

### 2. Cấu hình tài khoản

Điền đầy đủ thông tin vào file  `config/user.json`

### 3. Lấy BrowserID

- Mở file `broserid/index.html` trên trình duyệt.
- Copy giá trị `Visitor ID` (BrowserID) và điền vào biến `browser_id` trong `main.py` nếu muốn sử dụng BrowserID mới.

### 4. Chạy chương trình

```sh
python main.py
```

Kết quả sẽ trả về lịch sử giao dịch tài khoản.

## Lưu ý ⚠️

- ❗ Không chia sẻ thông tin tài khoản cho bất kỳ ai.
- 🚫 Không sử dụng project cho mục đích thương mại hoặc vi phạm pháp luật.
- 📚 Project chỉ mang tính chất nghiên cứu và học tập.

## Đóng góp 🤝

Mọi đóng góp, báo lỗi hoặc ý tưởng cải tiến xin gửi issue hoặc pull request.

---

**Tác giả:** LeVietHung  - Netrotion  
**Liên hệ:** [GitHub](https://github.com/netrotion)

## ☕ Buy me a coffee

Nếu bạn thấy dự án hữu ích và muốn ủng hộ tác giả, bạn có thể gửi đóng góp qua chuyển khoản:

- **Ngân hàng:** Vietcombank  
- **Số tài khoản:** 1057236828  
- **Chủ tài khoản:** Lê Việt Hùng