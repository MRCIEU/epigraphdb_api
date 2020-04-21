from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", response_model=bool)
def get_top_ping():
    """Test that you are connected to the API."""
    return True
