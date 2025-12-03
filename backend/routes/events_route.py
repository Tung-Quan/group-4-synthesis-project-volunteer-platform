from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models import event_models
from ..controllers import event_controller
from ..dependencies import get_current_user, require_types

router = APIRouter()

#-------------------------- SEARCH FOR EVENT ------------------------------
@router.get(
    "/search",
    response_model=list[event_models.SearchResult],
    status_code=status.HTTP_200_OK
)
def search_events(q: str):
    """
    API Search hoạt động theo từ khóa.
    Tìm theo: title, description, location, org_name.
    """
    results = event_controller.search_events(q)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return results

#-------------------------- EVENT APIs ------------------------------
@router.get("/get-all-event", response_model=list[event_models.EventResponse], status_code=status.HTTP_200_OK)
def get_events():
    result = event_controller.get_events()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.get("/get-own-event", response_model=list[event_models.EventResponse], status_code=status.HTTP_200_OK)
def get_own_events(current_user: dict = Depends(require_types("ORGANIZER"))):
    result = event_controller.get_own_events(str(current_user["id"]))
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.get("/upcoming", response_model=list[event_models.EventListResponse])
def get_upcoming_events():
    result = event_controller.get_upcoming_events()
    if result is None:
        return []
    return result

@router.get("/ongoing", response_model=list[event_models.EventListResponse])
def get_ongoing_events():
    result = event_controller.get_ongoing_events()
    if result is None:
        return []
    return result

@router.get("/{id}", response_model=event_models.EventDetail, status_code=status.HTTP_200_OK)
def get_event_by_id(id: str):
    result = event_controller.get_event_by_id(id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(
    request: event_models.EventRequest, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    results = event_controller.create_event(request, str(current_user["id"]))
    if results is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return results

@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_event_info(
    id: str, 
    request: event_models.UpdateEvent, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    result = event_controller.update_event_info(id, request, str(current_user["id"]))
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result

#  ------------------------------------------ APIP for EVENT_SLOTS ------------------------
@router.post("/{event_id}/create-slot", response_model=event_models.SlotResponse, status_code=status.HTTP_201_CREATED)
def create_event_slot(
    event_id: str, 
    request: event_models.SlotCreate, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    result, code = event_controller.add_slot_to_event(event_id, request, str(current_user["id"]))
    if code != 201:
        raise HTTPException(status_code=code, detail=result["message"])
    return result

@router.delete("/slots/{slot_id}", response_model=event_models.MessageResponse)
def delete_event_slot(
    slot_id: str, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    """Xóa một slot (Cần check xem có sinh viên đăng ký chưa)"""
    result, code = event_controller.delete_slot(slot_id, str(current_user["id"]))
    if code != 200:
        raise HTTPException(status_code=code, detail=result["message"])
    return result

@router.patch("/slots/{slot_id}", response_model=event_models.SlotResponse)
def update_event_slot(
    slot_id: str, 
    request: event_models.SlotUpdate, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    """Cập nhật thông tin slot (giờ, ngày, capacity...)"""
    result, code = event_controller.update_slot(slot_id, request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(status_code=code, detail=result["message"])
    return result

@router.get(
        "/slots/{slot_id}", 
        response_model=event_models.SlotResponse,
        status_code=status.HTTP_200_OK)
def get_slot_detail_route(
    slot_id: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Lấy chi tiết một Slot cụ thể.
    Public API (Ai cũng xem được để biết còn chỗ hay không).
    """
    result = event_controller.get_slot_detail(slot_id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Slot not found"
        )
    return result


