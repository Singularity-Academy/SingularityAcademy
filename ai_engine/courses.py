from sanic import Blueprint

from ai_engine.auth import AuthManager, login_required

bp = Blueprint("courses", url_prefix="/courses")

bp.ctx.auth = AuthManager

@bp.get("/all")
@login_required
async def get_courses(request):
    request.ctx.db