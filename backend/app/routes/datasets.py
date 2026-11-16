
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from io import BytesIO
import pandas as pd
import uuid
from app.services.quality import calculate_quality
from app.services.profiling import generate_profile
from fastapi import Form
from app.services.anomaly import detect_anomalies

router = APIRouter(prefix="/datasets", tags=["Dataset Analysis"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json"}
MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, XLSX and JSON files are supported."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 20 MB limit."
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    dataset_id = str(uuid.uuid4())

    try:
        buffer = BytesIO(content)

        if extension == ".csv":
            df = pd.read_csv(buffer)

        elif extension == ".xlsx":
            df = pd.read_excel(buffer)

        else:
            df = pd.read_json(buffer)

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset contains no records."
            )

        if len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="Dataset contains no columns."
            )

        profile = generate_profile(df)

        return {
            "message": "Dataset uploaded and analyzed successfully",
            "dataset_id": dataset_id,
            "filename": file.filename,
            "profile": profile
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to process dataset: {str(error)}"
        )

@router.post("/quality")
async def assess_dataset_quality(file: UploadFile = File(...)):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 20 MB limit."
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        buffer = BytesIO(content)

        if extension == ".csv":
            df = pd.read_csv(buffer)

        elif extension == ".xlsx":
            df = pd.read_excel(buffer)

        else:
            df = pd.read_json(buffer)

        if df.empty or len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="Dataset contains no records or columns."
            )

        quality_report = calculate_quality(df)

        return {
            "message": "Data quality assessment completed",
            "filename": file.filename,
            "report": quality_report
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Quality assessment failed: {str(error)}"
        )

@router.post("/anomalies")
async def analyze_anomalies(
    file: UploadFile = File(...),
    contamination: float = Form(0.05)
):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    if not 0 < contamination <= 0.5:
        raise HTTPException(
            status_code=400,
            detail="Contamination must be between 0 and 0.5."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 20 MB limit."
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:

        buffer = BytesIO(content)

        if extension == ".csv":
            df = pd.read_csv(buffer)

        elif extension == ".xlsx":
            df = pd.read_excel(buffer)

        else:
            df = pd.read_json(buffer)

        if df.empty or len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="Dataset contains no records or columns."
            )

        result = detect_anomalies(
            df,
            contamination=contamination
        )

        return {
            "message": "Anomaly detection completed successfully",
            "filename": file.filename,
            "report": result
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Anomaly detection failed: {str(error)}"
        )
