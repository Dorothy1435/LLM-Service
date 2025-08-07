import React, { useState } from 'react';
import axios from 'axios';
import './Analyst.css';

function Analyst() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const [studentId, setStudentId] = useState('');
  const [totalCredit, setTotalCredit] = useState('');
  const [majorCredit, setMajorCredit] = useState('');
  const [courses, setCourses] = useState('');
  const [gradResult, setGradResult] = useState(null);

  const [month, setMonth] = useState('');
  const [schedule, setSchedule] = useState([]);
  const [faqQuestion, setFaqQuestion] = useState('');
  const [faqAnswer, setFaqAnswer] = useState('');
  const [faqSource, setFaqSource] = useState('');

  const handleNoticeSubmit = async () => {
    if (!question.trim()) return;
    try {
      const res = await axios.post("http://localhost:8000/notice", {
        question: question
      });
      setAnswer(res.data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("⚠️ 서버 오류: 답변을 가져올 수 없습니다.");
    }
  };

  const handleGraduateSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:8000/graduate', {
        student_id: studentId,
        total_credit: parseInt(totalCredit),
        major_credit: parseInt(majorCredit),
        taken_courses: courses.split(',').map((c) => c.trim())
      });
      setGradResult(res.data);
    } catch (err) {
      console.error(err);
      setGradResult({ error: '오류가 발생했습니다. 서버를 확인하세요.' });
    }
  };

  const handleScheduleSubmit = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/schedule`, {
        params: { month: month }
      });
      setSchedule(res.data);
    } catch (err) {
      console.error(err);
      setSchedule([{ date: '', title: '⚠️ 일정 데이터를 불러오지 못했습니다.' }]);
    }
  };
  const handleFaqSubmit = async () => {
  if (!faqQuestion.trim()) return;

  try {
    const res = await axios.post("http://localhost:8000/faq", {
      question: faqQuestion
    });
    setFaqAnswer(res.data.answer);
    setFaqSource(res.data.source);
  } catch (error) {
    console.error(error);
    setFaqAnswer("⚠️ 서버 오류: 답변을 가져올 수 없습니다.");
    setFaqSource("error");
  }
};

  return (
    <div className="analyst-container">

      {/* 🔹 공지 응답 섹션 */}
      <div className="analyst-section">
        <h2 className="analyst-title">📢 공지 기반 질문</h2>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="예: 이번 주 휴강 있어?"
          className="analyst-input"
        />
        <button onClick={handleNoticeSubmit} className="analyst-button">
          질문하기
        </button>
        {answer && (
          <div className="analyst-answer">
            <p><strong>📌 GPT 응답:</strong><br />{answer}</p>
          </div>
        )}
      </div>

      {/* 🔸 졸업 판단 섹션 */}
      <div className="analyst-section">
        <h2 className="analyst-title">🎓 졸업 가능 여부 판단</h2>
        <input
          className="analyst-input"
          placeholder="학번"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        />
        <input
          className="analyst-input"
          placeholder="총 이수 학점"
          value={totalCredit}
          onChange={(e) => setTotalCredit(e.target.value)}
        />
        <input
          className="analyst-input"
          placeholder="전공 이수 학점"
          value={majorCredit}
          onChange={(e) => setMajorCredit(e.target.value)}
        />
        <input
          className="analyst-input"
          placeholder="이수 과목명 (쉼표로 구분)"
          value={courses}
          onChange={(e) => setCourses(e.target.value)}
        />
        <button onClick={handleGraduateSubmit} className="analyst-button">
          졸업 판단 요청
        </button>
        {gradResult && (
          <div className="analyst-answer">
            {gradResult.error ? (
              <p>{gradResult.error}</p>
            ) : (
              <>
                <p><strong>학번:</strong> {gradResult.student_id}</p>
                <p><strong>졸업 가능:</strong> {gradResult.graduation_possible ? '✅ 가능' : '❌ 불가능'}</p>
                <p><strong>학점 상태:</strong> {gradResult.credit_status}</p>
                <p><strong>미이수 필수 과목:</strong> {gradResult.missing_courses.length > 0 ? gradResult.missing_courses.join(', ') : '없음'}</p>
              </>
            )}
          </div>
        )}
      </div>

      {/* 📅 학과 일정 조회 섹션 */}
      <div className="analyst-section">
        <h2 className="analyst-title">📅 학과 일정 조회</h2>
        <input
          className="analyst-input"
          placeholder="예: 2025-08"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <button onClick={handleScheduleSubmit} className="analyst-button">
          일정 확인
        </button>
        {schedule.length > 0 && (
          <div className="analyst-answer">
            {schedule.map((item, idx) => (
              <p key={idx}>📌 <strong>{item.date}</strong>: {item.title}</p>
            ))}
          </div>
        )}
      </div>
      {/* 🤖 FAQ 질문 섹션 */}
<div className="analyst-section">
  <h2 className="analyst-title">🤖 자주 묻는 질문 (FAQ)</h2>
  <input
    className="analyst-input"
    placeholder="예: 복수전공 어떻게 신청해?"
    value={faqQuestion}
    onChange={(e) => setFaqQuestion(e.target.value)}
  />
  <button onClick={handleFaqSubmit} className="analyst-button">
    질문하기
  </button>

  {faqAnswer && (
    <div className="analyst-answer">
      <p><strong>📌 응답:</strong><br />{faqAnswer}</p>
      <p><em>출처: {faqSource === "faq" ? "📚 FAQ 데이터" : "🤖 GPT 응답"}</em></p>
    </div>
  )}
</div>

    </div>
  );
}

export default Analyst;
