const express = require('express');
const app = express();
app.use(express.json());

// 1. Database giả lập 
let books = [
    { id: 1, title: "Sách A", status: "Có sẵn" },
    { id: 2, title: "Sách B", status: "Có sẵn" }
];

// 2. POST: Thêm một cuốn sách mới
app.post('/api/books', (req, res) => {
    const newBook = { id: books.length + 1, ...req.body };
    books.push(newBook);
    res.status(201).json(newBook); 
});

// 3. GET: Lấy toàn bộ danh sách
app.get('/api/books', (req, res) => {
    res.status(200).json(books); // Trả về 2xx (200 OK)
});

// 4. PUT: Ghi đè toàn bộ thông tin
app.put('/api/books/:id', (req, res) => {
    const index = books.findIndex(b => b.id == req.params.id);
    if (index !== -1) {
        books[index] = { id: parseInt(req.params.id), ...req.body };
        res.json(books[index]);
    } else {
        res.status(404).json({ msg: "Không tìm thấy" }); // Trả về 4xx
    }
});

// 5. PATCH: Chỉ cập nhật trạng thái "Có sẵn" -> "Đã mượn"
app.patch('/api/books/:id', (req, res) => {
    const book = books.find(b => b.id == req.params.id);
    if (book) {
        book.status = req.body.status; 
        res.json(book);
    } else {
        res.status(404).send("Không tìm thấy sách");
    }
});

// 6. DELETE: Rút sách hỏng khỏi thư viện vĩnh viễn
app.delete('/api/books/:id', (req, res) => {
    books = books.filter(b => b.id != req.params.id);
    res.status(204).send(); 
});

// Xử lý lỗi hệ thống
app.use((err, req, res, next) => {
    res.status(500).json({ error: "Lỗi máy chủ!" });
});

app.listen(3000, () => console.log("Server running on port 3000"));