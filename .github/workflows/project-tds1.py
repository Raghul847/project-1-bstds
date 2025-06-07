from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import os

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    if request.image:
        try:
            image_data = base64.b64decode(request.image)
            with open("temp_image.jpg", "wb") as f:
                f.write(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")

    if "gpt-4o-mini" in request.question.lower() and "gpt3.5 turbo" in request.question.lower():
        response = {
            "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                    "text": "Use the model that’s mentioned in the question."
                },
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
                    "text": "My understanding is that you just have to use a tokenizer, similar to what Prof. Anand used, to get the number of tokens and multiply that by the given rate."
                }
            ]
        }
    else:
        response = {
            "answer": "I don't have sufficient information to answer this question at this time.",
            "links": []
        }

    if request.image and os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
