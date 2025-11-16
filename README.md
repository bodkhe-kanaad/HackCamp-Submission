# 🌟 PairUp – Learn Together, Grow Together  
### A social good platform that pairs students, keeps them accountable, and builds daily learning streaks.

PairUp tackles one of the most overlooked problems in student life: **academic isolation**.  
Many students don’t have study partners, feel disconnected in large courses, or struggle silently on their own.

PairUp creates a supportive learning habit by pairing students and giving them **one shared daily challenge** to stay accountable and learn together. With optional AI-generated questions powered by OpenAI, learning becomes personalized, consistent, and social.

---

## 📸 Demo Screenshots  
_(Add screenshots here once ready.)_

---

## 🚀 Features

### 🤝 Smart Student Pairing  
- Matches students based on **courses**, **interests**, and **shared learning goals**  
- Ensures relevant and meaningful study partnerships  
- Dynamic pairing using a custom similarity score

### 📘 Daily Shared Task  
- One multiple-choice question per day  
- Both partners must answer to continue their streak  
- Encourages daily learning in a low-stress, consistent way

### 🔥 Streak Tracking  
- Pairs build streaks together  
- Motivation through teamwork, accountability, and progress visibility

### 🤖 AI Mode (Optional)  
- Uses OpenAI to generate course-specific MCQs  
- RAG pipeline selects the best learning goal based on week & topic  
- Strict JSON validation ensures clean, safe, predictable LLM output  
- Fallback safety for uninterrupted user experience  

### 🎨 Beautiful UI  
- Modern, responsive, card-based UI  
- Clean dashboard, streak highlights, and interactive task screen  
- Smooth interaction patterns and simple navigation

---

## 🧠 The Social Good Impact

Learning is not just academic — it’s emotional and social.  
PairUp was built to support:

- Students who feel isolated in their programs  
- First-year and international students without peer networks  
- Anyone who studies better with consistency and accountability  
- Students who struggle with motivation and burnout

PairUp aims to **reduce isolation**, **build sustainable study habits**, and **make education more collaborative and equitable**.

---

## 🏛 Architecture Overview

### Backend
- Python + Flask  
- PostgreSQL database  
- Pair matching system  
- AI question generator  
- Shared LeetCode question pool  
- CRUD APIs for user, pairing, questions, and streaks

### AI System
- OpenAI GPT-4 / GPT-3.5 for question generation  
- Custom RAG pipeline:
  - ML classifier  
  - Embedding similarity  
  - Keyword overlap search  
- JSON validator + schema enforcement  
- Fallback logic to guarantee safe outputs

### Frontend
- React (Vite)  
- Card-based MCQ UI  
- Responsive design  
- Dashboard, pairing UI, daily task screen  
- Modern component-based styling

### DevOps
- GitHub Actions workflow for OpenAI key testing  
- Environment variables via `.env`  
- Secret key management through GitHub Secrets

---

## 🛠️ Built With

### **Frontend**
- React  
- Vite  
- Tailwind-inspired custom CSS  
- Styled components and card layout patterns  

### **Backend**
- Flask  
- PostgreSQL  
- psycopg2  
- Python 3.11  
- REST API endpoints  

### **AI / ML**
- OpenAI API  
- Embedding models  
- Custom prompt engineering  
- JSON extraction + validation  
- RAG selector  

### **Dev Tools**
- GitHub Actions  
- LM Studio (during development)  
- Postman for API testing  
- dotenv  
- Render / Railway (optional deployment)

---

## 📚 How It Works

### 1️⃣ User Signs Up  
They input:
- Name  
- Courses  
- Interests  
- Academic goal  

### 2️⃣ PairUp Algorithm Matches Them  

### 3️⃣ Daily Challenge System  
- Fetch today’s task  
- If no task exists → create one  
- Prevent double submissions  
- Track streak per pair

### 4️⃣ AI Mode (Optional)  
- System identifies the best learning goal for that course & week  
- OpenAI generates an MCQ  
- Question is validated and inserted  
- Delivered to both partners

---

## 🧩 Challenges We Overcame

- Getting AI to output strict JSON reliably  
- Designing an LLM fallback that doesn’t break user flow  
- Ensuring pairs cannot cheat by resubmitting  
- Handling streak logic in a robust way  
- Building a UI that feels calming, not overwhelming  
- Maintaining social-good focus while adding technical complexity  

---

## 🏁 Running Locally

```bash
cd backend
pip install -r requirements.txt
python app.py

create a .env file 
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_db_url

cd frontend
npm install
npm run dev
