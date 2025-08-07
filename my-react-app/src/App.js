import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Analyst from './Analyst'; // 새 페이지 불러오기

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>LLM 기반 챗봇 서비스</h1>
        <p>이 페이지는 대형 언어 모델(LLM)을 기반으로 작동하는 챗봇 서비스입니다.</p>
        <Link to="/analyst" className="start-button">시작</Link>
      </header>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyst" element={<Analyst />} />
      </Routes>
    </Router>
  );
}

export default App;
