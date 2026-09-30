from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, save_user, save_plan, update_plan, get_user, get_all_users
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from fastapi.templating import Jinja2Templates
import os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- Pydantic Schemas ---
class UserInput(BaseModel):
    username: str
    user_id: int
    age: int
    weight: int
    goal: str
    intensity: str

class FeedbackRequest(BaseModel):
    user_id: int
    feedback: str

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    # Save user
    user_data = {"id": user_id, "name": username, "age": age, "weight": weight, "goal": goal, "intensity": intensity}
    user = save_user(db, user_data)

    # Generate workout + nutrition tip
    workout_plan = generate_workout_gemini(goal, intensity)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Save plan
    save_plan(db, user.id, workout_plan)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": user,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip
    })

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)
    updated_plan_text = update_workout_plan(user.original_plan, feedback)
    update_plan(db, user.id, updated_plan_text)
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": user,
        "workout_plan": updated_plan_text,
        "nutrition_tip": nutrition_tip
    })

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})




templates = Jinja2Templates(directory=TEMPLATE_DIR)
