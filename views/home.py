import fastapi

router = fastapi.APIRouter()


@router.get('/')
def index():
    # TODO: Add something sensible for the root.
    return "Move along ... "


@router.get('/favicon.ico')
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/images/favicon.ico')
