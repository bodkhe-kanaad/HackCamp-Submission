import { api } from "./api";

export async function getRandomQuestion() {
  const res = await api.get("/question");
  return res.data;
}

export async function checkAnswer(question_id, choice) {
  const res = await api.post("/check-answer", {
    question_id,
    choice
  });
  return res.data.correct;
}
