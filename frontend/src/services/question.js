import { api } from "./api";

export async function getRandomQuestion() {
  const res = await api.get("/question");
  return res.data;
}

export async function checkAnswer(id, choice) {
  const res = await api.post("/check-answer", {
    id,
    choice
  });
  return res.data.correct;
}
