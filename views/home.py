import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates('templates')
router = fastapi.APIRouter()


@router.get('/', include_in_schema=False)
def index(request: Request):
    data = {'request': request}
    return templates.TemplateResponse('home/index.html', data)


@router.get('/favicon.ico', include_in_schema=False)
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/images/favicon.ico')
