from sanic import Blueprint
from ai_engine.apps.auth import login_required
from ai_engine.apps.courses.models import Course
from sanic.response import json

bp = Blueprint("courses", url_prefix="/courses")

@bp.get("/")
@login_required
async def get_courses(request):
    user_id = request.ctx.user_id
    courses = await Course.filter(user_id=user_id).all()
    data = [{"id": course.id, "name": course.name, "description": course.description} for course in courses]
    return json(data)