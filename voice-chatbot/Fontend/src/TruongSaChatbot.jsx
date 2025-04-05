import React, { useState } from "react";

export default function TruongSaChatbot() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [action, setAction] = useState("login");

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div className="w-1/4 bg-gray-800 p-6">
        <h2 className="text-lg font-semibold mb-4">Đăng nhập hoặc đăng ký</h2>

        <div className="mb-4">
          <label className="block mb-1">Select Action</label>
          <select
            className="w-full bg-gray-700 text-white p-2 rounded"
            value={action}
            onChange={(e) => setAction(e.target.value)}
          >
            <option value="login">Đăng nhập</option>
            <option value="register">Tạo tài khoản mới</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block mb-1">Nhập E-mail</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 bg-gray-700 text-white rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1">Nhập Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 bg-gray-700 text-white rounded"
          />
        </div>

        <button className="w-full bg-green-600 hover:bg-green-700 p-2 rounded">
          Bấm enter để đăng nhập
        </button>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 p-10">
        <h1 className="text-2xl font-bold mb-6">
          Chatbot hỏi đáp các câu hỏi liên quan đến mô hình đảo Trường Sa lớn
        </h1>

        <div className="space-y-4 max-w-2xl">
          <div className="bg-gray-700 p-4 rounded-xl">
            <p className="font-semibold">🧍 Tôi có thể giúp gì cho bạn?</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-xl">
            <p className="font-semibold">🧍 Giới thiệu cho tôi về mô hình đảo Trường Sa lớn?</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-xl">
            <p>
              Mô hình đảo Trường Sa lớn là một mô hình đảo nhân tạo được xây dựng trên đảo Trường Sa Lớn,
              quần đảo Trường Sa, Việt Nam. Mô hình này có quy mô lớn, diện tích khoảng 1 km², với nhiều
              công trình hạ tầng như nhà ở, trung tâm y tế, trạm y tế, nhà ở cho cán bộ trên đảo...
              <br />
              Mô hình đảo Trường Sa lớn được xây dựng với mục đích như: Tăng cường tiềm lực về chủ
              quyền biển đảo của Việt Nam trên biển Đông. Giúp các đơn vị và dân cư trên đảo có điều kiện
              sinh sống và làm việc tốt hơn, mô phỏng môi trường thực tế. Phát triển tiềm năng du lịch,
              nâng cao đời sống của cán bộ trên đảo, nâng cao khả năng an toàn cho người dân và cán bộ...
              <br />
              Mô hình đảo Trường Sa lớn cũng có một phần hiển hiện và phát triển bền vững trên vùng biển
              Đông, góp phần nâng cao sức mạnh của Việt Nam trên vùng biển này.
            </p>
          </div>
        </div>

        <div className="mt-6">
          <input
            placeholder="Your message"
            className="w-full p-3 bg-gray-800 text-white rounded"
          />
        </div>
      </div>
    </div>
  );
}
