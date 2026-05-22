# from fastapi import APIRouter, HTTPException, Depends
# from firebase_admin import firestore
# from models.user import User
# from auth_utils import require_role

# router = APIRouter(prefix="/users", tags=["Users"])


# @router.patch("/{user_id}/disable", dependencies=[Depends(require_role("admin"))])
# async def disable_user(user_id: str):
#     try:
#         db = firestore.client()
#         user_ref = db.collection('users').document(user_id)
#         user_doc = user_ref.get()

#         if not user_doc.exists:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado en Sucre")

#         # Actualizamos el estado a inactivo
#         user_ref.update({"is_active": False})
        
#         return {"status": "success", "message": f"Usuario {user_id} inhabilitado correctamente"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
from fastapi import APIRouter, HTTPException, Depends
from firebase_admin import firestore
from auth_utils import require_role

router = APIRouter(prefix="/users", tags=["Users"])

# [READ] Obtener lista de todos los usuarios (Para el Admin)
@router.get("/")
async def list_users():
    db = firestore.client()
    users = db.collection("users").stream()
    return [u.to_dict() for u in users]

# [READ] Obtener un usuario específico por ID
@router.get("/{user_id}")
async def get_user(user_id: str):
    db = firestore.client()
    user_ref = db.collection('users').document(user_id).get()
    if not user_ref.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_ref.to_dict()

# [UPDATE] Inhabilitar un usuario (Update de estado)
@router.patch("/{user_id}/disable")
async def disable_user(user_id: str):
    db = firestore.client()
    user_ref = db.collection('users').document(user_id)
    if not user_ref.get().exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_ref.update({"is_active": False})
    return {"message": "Usuario inhabilitado correctamente"}

# [DELETE] Eliminar un usuario de la base de datos
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    db = firestore.client()
    db.collection('users').document(user_id).delete()
    return {"message": "Usuario eliminado correctamente"}