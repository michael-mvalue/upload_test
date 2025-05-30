from fastapi import FastAPI, File, UploadFile
import boto3
import uuid

app = FastAPI()

# Initialize S3 client (uses IAM role if on EC2)
s3 = boto3.client("s3")
BUCKET_NAME = "gto-presolves"

@app.post("/upload")
async def upload_to_s3(file: UploadFile = File(...)):
    file_content = await file.read()
    file_key = f"uploads/{uuid.uuid4()}_{file.filename}"

    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=file_key, Body=file_content)
        return {"message": "Upload successful", "s3_key": file_key}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def test():
    return {"message": "Server is working!"}

@app.get("/test")
async def test():
    return {"message": "🤩🤩🤩"}