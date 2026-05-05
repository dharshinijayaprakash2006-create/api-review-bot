from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

# Checklist items
checklist = [
    "Proper routing",
    "Input validation",
    "Error handling",
    "Authentication",
    "Status codes"
]

def analyze_code(code: str):
    issues = []
    passed = []
    score = 0

    # Check 1: Proper routing
    if "@app." in code:
        passed.append("✅ Proper routing found")
        score += 2
    else:
        issues.append("❌ No proper routing found")

    # Check 2: Input validation
    if "UploadFile" in code or "BaseModel" in code or "validate" in code.lower():
        passed.append("✅ Input validation found")
        score += 2
    else:
        issues.append("❌ No input validation found")

    # Check 3: Error handling
    if "try" in code and "except" in code:
        passed.append("✅ Error handling found")
        score += 2
    else:
        issues.append("❌ No error handling (try-except missing)")

    # Check 4: Authentication
    if "auth" in code.lower() or "token" in code.lower() or "jwt" in code.lower():
        passed.append("✅ Authentication found")
        score += 2
    else:
        issues.append("⚠ No authentication implemented")

    # Check 5: Status codes
    if "status_code" in code or "HTTPException" in code:
        passed.append("✅ Proper status codes used")
        score += 2
    else:
        issues.append("⚠ No HTTP status codes used")

    return passed, issues, score


# Home route
@app.get("/")
def home():
    return {"message": "API Review Bot Running"}


# Upload API
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    return {
        "filename": file.filename,
        "preview": text[:200]
    }


# Review API with Checklist
@app.post("/review/")
async def review(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    passed, issues, score = analyze_code(code)

    return {
        "filename": file.filename,
        "checklist": checklist,
        "passed": passed,
        "issues": issues,
        "score": f"{score}/10",
        "suggestions": [
            "Use try-except for error handling",
            "Validate all user inputs",
            "Return proper HTTP status codes",
            "Add authentication if needed",
            "Follow REST API best practices"
        ]
    }


# Report API
@app.post("/report/")
async def report(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    passed, issues, score = analyze_code(code)

    report_text = f"""
API REVIEW BOT - CODE REVIEW REPORT
=====================================
Filename: {file.filename}
Score: {score}/10

PASSED CHECKS:
{chr(10).join(passed)}

ISSUES FOUND:
{chr(10).join(issues) if issues else "No issues found"}

SUGGESTIONS:
- Use try-except for error handling
- Validate all user inputs
- Return proper HTTP status codes
- Add authentication if needed
- Follow REST API best practicesgit add .
=====================================
    """

    return {"report": report_text}