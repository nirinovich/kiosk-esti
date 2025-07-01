# K’iosk POS

K’iosk is a modern, open-source Point of Sale (POS) system built entirely with Python and [Kivy](https://kivy.org/) framework.  
It is designed for grocery stores and small retailers, focusing on simplicity, security, and extensibility.

---

## 🚀 Features

- **User Authentication** (secure login with hashed passwords)
- **Intuitive Dashboard** (touch-friendly, easy navigation)
- **SQLite3 Database** (local, reliable storage)
- **Product & Inventory Management** (planned)
- **Sales Processing** (planned)
- **Cross-platform** (Windows, Linux, macOS, Raspberry Pi)

---

## 📦 Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/nirinovich/pos-kivy.git
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python src/main.py
   ```

---

## 🛡️ Security

- Passwords are hashed using `bcrypt` before storage.
- No plaintext credentials are stored.
- User input is validated throughout the app.

---

## 🗺️ Roadmap

### MVP (Minimum Viable Product)
- [x] Secure user login (bcrypt)
- [x] SQLite3 database initialization
- [x] Simple test screen after login

### v0.2
- [x] Dashboard UI (New Sale, Inventory, Reports, Settings)
- [x] Product management (add/edit/delete products)
- [x] Upgrade to KivyMD

### v0.3
- [ ] Sales processing (scan/add products, calculate totals, print receipts)
- [ ] Basic sales reporting (daily/weekly/monthly)
- [ ] User roles (admin/cashier)

### v0.4
- [ ] Settings page (store info, tax rates, etc.)
- [ ] Improved error handling and notifications
- [ ] Responsive design for tablets/touchscreens

### v1.0
- [ ] Full-featured POS for grocery stores
- [ ] Export/import data (CSV, Excel)
- [ ] Multi-user support
- [ ] Basic offline/online sync (optional)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 💡 Inspiration

K’iosk is inspired by the need for simple, affordable, and customizable POS solutions for small businesses.
