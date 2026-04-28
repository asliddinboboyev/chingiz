"""
TABIB AI — Medical Expert Chatbot
Run: uvicorn main:app --port 8000
"""

import os
from dotenv import load_dotenv
load_dotenv()

import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tabib AI ishlayapti 🚀"}
import anthropic


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"

app = FastAPI(title="Tabib AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SYSTEM_PROMPT = """Sen TABIB AI — O'zbekistondagi tibbiy ekspert.

FORMAT: HTML formatda javob ber.
Foydalan: <b>matn</b>, <br>

ROLLAR:
1. EKSPERT: Aniq doza, mexanizm, yon ta'sir
2. MOTIVATOR: Bemorni ilhomlantirish

SHOSHILINCH:
"<span style='color:#e74c3c'><b>DARHOL 103 ga qo'ng'iroq qiling!</b></span>"

Til: O'zbek"""

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)

@app.post("/chat")
async def chat(req: ChatRequest):
    if not ANTHROPIC_API_KEY:
        raise HTTPException(503, "API key yo'q")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": req.message}]
    )
    
    reply = response.content[0].text.strip()
    reply = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", reply)
    reply = re.sub(r"^[-*]\s+(.+)$", r"• \1", reply)
    
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
