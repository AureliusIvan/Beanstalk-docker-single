from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.utility_digitilization.utils.ocr_util.ocr_util import process_pdf

router = APIRouter()


@router.get("/test")
async def test_utility():
    """ Test the Utility Digitilization API """
    return JSONResponse(content={
        "message": "Utility Digitilization API is working.",
        "status": "success"
    })


@router.post("/ocr")
async def pdf_ocr(file: UploadFile = File(...)):
    """
    This function is used to extract text from pdf
    :param file: pdf file
    :return: extracted text
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Please upload a PDF file.")

        # Read the file bytes
        pdf_bytes = await file.read()

        # Validate the file is a PDF
        if not pdf_bytes.startswith(b'%PDF'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF file.")

        # Process the PDF
        result = await process_pdf(pdf_bytes)
        return JSONResponse(content={
            "result": result,
            "message": "PDF processed successfully.",
            "status": "success"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
