from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import json
from prompt_builder import build_cppt_prompt
from ai_services.gemini_openrouter import generate_from_gemini
from ai_services.deepseek import generate_from_deepseek

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Scribe AI API",
    description="API untuk membantu dokter membuat catatan CPPT menggunakan AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Diagnosis(BaseModel):
    code_icd: str
    diagnosa: str

class Procedure(BaseModel):
    code_icd: str
    diagnosa: str

class CPPTData(BaseModel):
    subject: str
    object: str
    assessment: str
    plan: str
    instruction: str
    evaluation: str
    rekom_diagnosa_utama: List[Diagnosis]
    rekom_prosedur_utama: List[Procedure]

class CPPTResponse(BaseModel):
    code: int = Field(..., description="Response code")
    message: str = Field(..., description="Response message")
    data: Optional[CPPTData] = Field(None, description="Response data")

class CPPTRequest(BaseModel):
    input_text: str = Field(..., min_length=10, description="Input teks dari dokter")
    provider: str = Field(default="gemini", description="Provider AI yang digunakan (gemini/deepseek)")

    class Config:
        schema_extra = {
            "example": {
                "input_text": "Pasien datang dengan keluhan demam 3 hari, batuk, dan pilek. Suhu 38.5°C, nadi 90x/menit, RR 20x/menit. Pemeriksaan fisik: faring hiperemis, tonsil membesar. Rencana: paracetamol 3x500mg, istirahat cukup.",
                "provider": "gemini"
            }
        }

@app.get("/")
async def root():
    return {
        "code": 200,
        "message": "Selamat datang di Medical Scribe AI API",
        "data": {
            "endpoints": {
                "/generate-cppt": "POST - Generate catatan CPPT",
                "/docs": "GET - Dokumentasi API (Swagger UI)"
            }
        }
    }

@app.post("/generate-cppt", response_model=CPPTResponse)
async def generate_cppt(request: CPPTRequest):
    """
    Generate catatan CPPT berdasarkan input dokter.
    
    Args:
        request (CPPTRequest): Request body yang berisi input teks dan provider AI
        
    Returns:
        CPPTResponse: Hasil generate CPPT dalam format terstruktur
        
    Raises:
        HTTPException: Jika terjadi error saat generate CPPT
    """
    try:
        logger.info(f"Generating CPPT using provider: {request.provider}")
        prompt = build_cppt_prompt(request.input_text)

        if request.provider.lower() == "gemini":
            result = generate_from_gemini(prompt)
        elif request.provider.lower() == "deepseek":
            result = generate_from_deepseek(prompt)
        else:
            return CPPTResponse(
                code=400,
                message="Provider AI tidak dikenal. Gunakan 'gemini' atau 'deepseek'"
            )

        # Parse the JSON response
        try:
            parsed_result = json.loads(result.replace("```json", "").replace("```", ""))
            if "data" not in parsed_result:
                return CPPTResponse(
                    code=500,
                    message="Response tidak memiliki field 'data'"
                )
            
            # Validate the response structure
            response_data = CPPTResponse(
                code=200,
                message="CPPT berhasil digenerate",
                data=CPPTData(**parsed_result["data"])
            )
            
            logger.info("CPPT generated successfully")
            return response_data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {str(e)}")
            return CPPTResponse(
                code=500,
                message="Response dari AI tidak dalam format JSON yang valid"
            )
        except ValueError as e:
            logger.error(f"Invalid response structure: {str(e)}")
            return CPPTResponse(
                code=500,
                message=f"Struktur response tidak valid: {str(e)}"
            )

    except Exception as e:
        logger.error(f"Error generating CPPT: {str(e)}")
        return CPPTResponse(
            code=500,
            message=f"Terjadi kesalahan saat generate CPPT: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
