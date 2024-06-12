import streamlit as st
import requests
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

# Define los esquemas necesarios
class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    dni: int = Field(..., ge=1000, le=999999999999, description="DNI of the user")
    password: str = Field(..., min_length=5, max_length=50, description="Password of the user")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserOut(BaseModel):
    user_id: UUID
    dni: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

API_URL = "http://127.0.0.1:8000/api/v1"  # Reemplaza con tu URL de FastAPI

# Estado de la sesión para manejar autenticación
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

def login_user(dni: int, password: str):
    form_data = {
        "username": dni,
        "password": password
    }
    response = requests.post(f"{API_URL}/auth/login", data=form_data)
    if response.status_code == 200:
        tokens = TokenSchema(**response.json())
        st.session_state.access_token = tokens.access_token
        st.session_state.logged_in = True
        st.experimental_rerun()
    else:
        st.error("Invalid DNI or password")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.access_token = None
    st.experimental_rerun()

def create_user(data: UserAuth):
    response = requests.post(f"{API_URL}/user/create", json=data.dict())
    if response.status_code == 200:
        st.success("Usuario creado con éxito")
    else:
        st.error(f"Error: {response.json().get('detail')}")

st.title("Gestión de Usuarios")

# Muestra el formulario de login o registro dependiendo del estado de la sesión
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Iniciar sesión", "Crear usuario"])

    with tab1:
        st.header("Iniciar sesión")
        dni = st.number_input("DNI", min_value=1000, max_value=999999999999)
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            login_user(dni, password)

    with tab2:
        st.header("Crear un nuevo usuario")
        email = st.text_input("Email")
        dni_reg = st.number_input("DNI para registro", min_value=1000, max_value=999999999999)
        password_reg = st.text_input("Contraseña para registro", type="password")

        if st.button("Crear usuario"):
            user_data = UserAuth(email=email, dni=dni_reg, password=password_reg)
            create_user(user_data)
else:
    st.header("Detalles del usuario actual")

    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{API_URL}/user/me", headers=headers)
    
    if response.status_code == 200:
        user = UserOut(**response.json())
        st.json(user.dict())
    else:
        st.error(f"Error: {response.json().get('detail')}")

    st.header("Actualizar usuario")

    email = st.text_input("Nuevo Email (opcional)")
    first_name = st.text_input("Nuevo Nombre (opcional)")
    last_name = st.text_input("Nuevo Apellido (opcional)")

    if st.button("Actualizar usuario"):
        update_data = UserUpdate(email=email, first_name=first_name, last_name=last_name)
        response = requests.post(f"{API_URL}/user/update", headers=headers, json=update_data.dict(exclude_none=True))
        
        if response.status_code == 200:
            st.success("Usuario actualizado con éxito")
        else:
            st.error(f"Error: {response.json().get('detail')}")

    if st.button("Cerrar sesión"):
        logout_user()
