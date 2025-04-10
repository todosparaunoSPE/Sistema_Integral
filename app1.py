# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 12:10:41 2025

@author: jperezr
"""

import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import calendar
from streamlit_calendar import calendar as st_calendar
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Planificación Estratégica PENSIONISSSTE",
    page_icon="📅",
    layout="wide"
)

# =============================================
# DATOS INICIALES (se almacenan en session_state)
# =============================================

if 'proyectos' not in st.session_state:
    st.session_state.proyectos = {
        "Jefatura Servicios de Planeación y Proyección financiera": [
            {
                "id": 1, 
                "nombre": "Análisis de tendencias económicas 2025-2030", 
                "responsable": "Dra. Laura Méndez", 
                "fecha_inicio": date(2024, 1, 15), 
                "fecha_entrega": date(2024, 6, 30), 
                "estado": "En progreso",
                "etapas": [
                    {"nombre": "Recopilación datos", "inicio": date(2024, 1, 15), "fin": date(2024, 2, 15), "completado": 100},
                    {"nombre": "Análisis inicial", "inicio": date(2024, 2, 16), "fin": date(2024, 4, 15), "completado": 75},
                    {"nombre": "Validación", "inicio": date(2024, 4, 16), "fin": date(2024, 5, 15), "completado": 0},
                    {"nombre": "Informe final", "inicio": date(2024, 5, 16), "fin": date(2024, 6, 30), "completado": 0}
                ]
            },
            {
                "id": 2, 
                "nombre": "Estudio de escenarios post-pandemia", 
                "responsable": "Lic. Carlos Rojas", 
                "fecha_inicio": date(2024, 3, 1), 
                "fecha_entrega": date(2024, 8, 15), 
                "estado": "En revisión",
                "etapas": [
                    {"nombre": "Revisión bibliográfica", "inicio": date(2024, 3, 1), "fin": date(2024, 3, 31), "completado": 100},
                    {"nombre": "Entrevistas expertos", "inicio": date(2024, 4, 1), "fin": date(2024, 5, 15), "completado": 90},
                    {"nombre": "Modelado escenarios", "inicio": date(2024, 5, 16), "fin": date(2024, 7, 15), "completado": 30},
                    {"nombre": "Redacción informe", "inicio": date(2024, 7, 16), "fin": date(2024, 8, 15), "completado": 0}
                ]
            }
        ],
        "Jefatura de Servicios de Estudios y Evaluación de la Competitividad": [
            {
                "id": 3, 
                "nombre": "Plan Estratégico Institucional 2025-2028", 
                "responsable": "Lic. Fernando Castro", 
                "fecha_inicio": date(2024, 2, 1), 
                "fecha_entrega": date(2024, 11, 30), 
                "estado": "En progreso",
                "etapas": [
                    {"nombre": "Diagnóstico institucional", "inicio": date(2024, 2, 1), "fin": date(2024, 4, 30), "completado": 80},
                    {"nombre": "Definición objetivos", "inicio": date(2024, 5, 1), "fin": date(2024, 6, 30), "completado": 20},
                    {"nombre": "Diseño estrategias", "inicio": date(2024, 7, 1), "fin": date(2024, 9, 30), "completado": 0},
                    {"nombre": "Documentación final", "inicio": date(2024, 10, 1), "fin": date(2024, 11, 30), "completado": 0}
                ]
            }
        ],
        "Jefatura del Bienestar": [
            {
                "id": 4, 
                "nombre": "Modelo financiero quinquenal", 
                "responsable": "CP. Ricardo Torres", 
                "fecha_inicio": date(2024, 1, 10), 
                "fecha_entrega": date(2024, 5, 31), 
                "estado": "En progreso",
                "etapas": [
                    {"nombre": "Recopilación datos históricos", "inicio": date(2024, 1, 10), "fin": date(2024, 2, 10), "completado": 100},
                    {"nombre": "Análisis tendencias", "inicio": date(2024, 2, 11), "fin": date(2024, 3, 15), "completado": 70},
                    {"nombre": "Modelado proyecciones", "inicio": date(2024, 3, 16), "fin": date(2024, 4, 30), "completado": 30},
                    {"nombre": "Validación y ajustes", "inicio": date(2024, 5, 1), "fin": date(2024, 5, 31), "completado": 0}
                ]
            }
        ]
    }

usuarios = {
    "Jefatura Servicios de Planeación y Proyección financiera": [
        {"username": "director_prospectiva", "nombre": "Dra. Laura Méndez", "rol": "Directora"},
        {"username": "analista1_prospectiva", "nombre": "Lic. Carlos Rojas", "rol": "Analista Senior"},
        {"username": "analista2_prospectiva", "nombre": "Mtro. Javier Soto", "rol": "Analista"},
        {"username": "investigador1", "nombre": "Dra. Ana Vargas", "rol": "Investigadora"},
        {"username": "coordinador_estudios", "nombre": "Lic. Roberto Núñez", "rol": "Coordinador"}
    ],
    "Jefatura de Servicios de Estudios y Evaluación de la Competitividad": [
        {"username": "director_planeacion", "nombre": "Lic. Fernando Castro", "rol": "Director"},
        {"username": "planificador1", "nombre": "Mtro. Adrián López", "rol": "Planificador Estratégico"},
        {"username": "planificador2", "nombre": "Lic. Sofía Ramírez", "rol": "Planificador"},
        {"username": "evaluador1", "nombre": "Dr. Omar Contreras", "rol": "Evaluador"},
        {"username": "coordinador_planeacion", "nombre": "Lic. Patricia Flores", "rol": "Coordinadora"}
    ],
    "Jefatura del Bienestar": [
        {"username": "director_finanzas", "nombre": "CP. Ricardo Torres", "rol": "Director"},
        {"username": "financiero1", "nombre": "Lic. Daniel Ortega", "rol": "Analista Financiero"},
        {"username": "financiero2", "nombre": "C.P. Mariana Jiménez", "rol": "Especialista"},
        {"username": "modelador1", "nombre": "Mtro. Luis Herrera", "rol": "Modelador"},
        {"username": "coordinador_finanzas", "nombre": "Lic. Gabriela Ruiz", "rol": "Coordinadora"}
    ]
}

# =============================================
# FUNCIONES AUXILIARES
# =============================================

def cargar_proyectos(departamento):
    """Carga los proyectos desde session_state"""
    return st.session_state.proyectos.get(departamento, [])

def autenticar_usuario():
    """Maneja la autenticación de usuarios"""
    st.sidebar.title("Sistema Integrado de la subdirección de Planeación Estratégica")
    st.sidebar.text("Desarrollado por: Javier Horacio Pérez Ricárdez")
    st.sidebar.text("Acceso al Sistema")
    departamento = st.sidebar.selectbox("Departamento", list(usuarios.keys()))
    
    usuarios_departamento = [f"{u['nombre']} ({u['username']})" for u in usuarios[departamento]]
    usuario_seleccionado = st.sidebar.selectbox("Usuario", usuarios_departamento)
    
    username = usuario_seleccionado.split("(")[1].replace(")", "")
    password = st.sidebar.text_input("Contraseña", type="password")
    
    
    
    
    
    if st.sidebar.button("Ingresar"):
        if password:  # Validación simulada
            usuario = next(u for u in usuarios[departamento] if u['username'] == username)
            
            st.session_state['autenticado'] = True
            st.session_state['departamento'] = departamento
            st.session_state['usuario'] = usuario['nombre']
            st.session_state['username'] = username
            st.session_state['rol'] = usuario['rol']
            st.sidebar.success(f"Bienvenido {usuario['nombre']}")
                
        else:
            st.sidebar.error("Contraseña incorrecta")
                
    return 'autenticado' in st.session_state

    

def mostrar_calendario_mensual(proyectos, mes=date.today().month, año=date.today().year):
    """Muestra un calendario mensual con hitos de proyectos"""
    cal = calendar.monthcalendar(año, mes)
    month_name = calendar.month_name[mes]
    
    st.subheader(f"Calendario de {month_name} {año}")
    
    # Crear un grid de calendario con Streamlit columns
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    cols = st.columns(7)
    
    for i, dia in enumerate(dias_semana):
        cols[i].write(f"**{dia}**")
    
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                current_date = date(año, mes, dia)
                eventos = []
                
                for proyecto in proyectos:
                    if proyecto['fecha_inicio'] == current_date:
                        eventos.append(f"🟢 {proyecto['nombre'][:15]}...")
                    if proyecto['fecha_entrega'] == current_date:
                        eventos.append(f"🔴 {proyecto['nombre'][:15]}...")
                    
                    for etapa in proyecto.get('etapas', []):
                        if etapa['inicio'] == current_date:
                            eventos.append(f"🟡 {etapa['nombre'][:12]}...")
                        if etapa['fin'] == current_date:
                            eventos.append(f"🟠 {etapa['nombre'][:12]}...")
                
                if current_date == date.today():
                    cols[i].markdown(f"<div style='background-color:#FFF3CD; border-radius:5px; padding:5px;'><b>{dia}</b></div>", unsafe_allow_html=True)
                else:
                    cols[i].write(f"**{dia}**")
                
                for evento in eventos[:3]:  # Mostrar máximo 3 eventos por día
                    cols[i].write(evento)
                if len(eventos) > 3:
                    cols[i].write(f"...+{len(eventos)-3}")


##########


def mostrar_timeline_proyecto(proyecto):
    """Muestra una línea de tiempo interactiva para un proyecto"""
    if 'etapas' not in proyecto or len(proyecto['etapas']) == 0:
        st.warning("Este proyecto no tiene etapas definidas")
        return
    
    # Convertir a DataFrame
    df = pd.DataFrame(proyecto['etapas'])
    
    # Asegurar que las fechas sean datetime
    df['inicio'] = pd.to_datetime(df['inicio'])
    df['fin'] = pd.to_datetime(df['fin'])
    
    # Calcular porcentaje de días transcurridos
    hoy = pd.to_datetime(date.today())
    df['porcentaje_transcurrido'] = df.apply(
        lambda x: min(100, max(0, ((hoy - x['inicio']).days / max(1, (x['fin'] - x['inicio']).days)) * 100)),
        axis=1
    )
    
    # Crear el gráfico de timeline
    fig = px.timeline(
        df,
        x_start="inicio",
        x_end="fin",
        y="nombre",
        color="completado",
        color_continuous_scale=[[0, '#FFA07A'], [0.5, '#FFD700'], [1, '#98FB98']],
        title=f"Línea de Tiempo - {proyecto['nombre']}",
        hover_data={
            "completado": ":.0f%",
            "porcentaje_transcurrido": ":.0f%",
            "inicio": "|%d/%m/%Y",
            "fin": "|%d/%m/%Y"
        }
    )
    
    # Añadir línea vertical para el día actual
    fig.add_vline(x=hoy, line_dash="dash", line_color="red")
    
    # Configuraciones adicionales
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="",
        hovermode="closest"
    )
    
    st.plotly_chart(fig, use_container_width=True)




    
def mostrar_calendario_interactivo(proyectos):
    """Calendario interactivo con todos los proyectos"""
    st.subheader("Calendario Interactivo de Proyectos")
    
    # Convertir proyectos a eventos para el calendario
    events = []
    color_map = {
        "En progreso": "#4285F4",
        "Pendiente": "#EA4335",
        "Completado": "#34A853",
        "En revisión": "#FBBC05",
        "Atrasado": "#000000"
    }
    
    for proyecto in proyectos:
        events.append({
            "title": f"📌 {proyecto['nombre']}",
            "start": proyecto['fecha_inicio'].strftime("%Y-%m-%d"),
            "end": (proyecto['fecha_entrega'] + timedelta(days=1)).strftime("%Y-%m-%d"),
            "color": color_map.get(proyecto['estado'], "#4285F4"),
            "allDay": True,
            "extendedProps": {
                "responsable": proyecto['responsable'],
                "estado": proyecto['estado']
            }
        })
        
        for etapa in proyecto.get('etapas', []):
            events.append({
                "title": f"➡️ {etapa['nombre']}",
                "start": etapa['inicio'].strftime("%Y-%m-%d"),
                "end": (etapa['fin'] + timedelta(days=1)).strftime("%Y-%m-%d"),
                "color": "#34A853",
                "allDay": True
            })
    
    # Configuración del calendario
    calendar_options = {
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "dayGridMonth",
        "nowIndicator": True,
        "eventClick": """function(info) {
            alert('Proyecto: ' + info.event.title + '\\nResponsable: ' + 
                  info.event.extendedProps.responsable + '\\nEstado: ' + 
                  info.event.extendedProps.estado);
        }"""
    }
    
    # Mostrar calendario
    st_calendar(
        events=events,
        options=calendar_options,
        custom_css="""
            .fc-event {
                cursor: pointer;
                font-size: 0.8em;
                padding: 2px;
            }
        """,
        key="proyectos_calendar"
    )

# =============================================
# PÁGINAS PRINCIPALES
# =============================================

def mostrar_dashboard_personalizado():
    """Página principal con resumen y calendarios"""
    departamento = st.session_state['departamento']
    proyectos = cargar_proyectos(departamento)
    
    st.title(f"📊 Panel de Control - {departamento}")
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    hoy = date.today()
    
    with col1:
        proyectos_activos = len([p for p in proyectos if p['estado'] in ["En progreso", "En revisión"]])
        st.metric("Proyectos Activos", proyectos_activos)
    
    with col2:
        proyectos_atrasados = len([p for p in proyectos if p['estado'] == "Atrasado"])
        st.metric("Proyectos Atrasados", proyectos_atrasados, delta_color="inverse")
    
    with col3:
        entregas_proximas = len([p for p in proyectos if p['fecha_entrega'] >= hoy and (p['fecha_entrega'] - hoy).days <= 15])
        st.metric("Entregas Próximas (15 días)", entregas_proximas)
    
    with col4:
        porcentaje_completado = sum(p['etapas'][0]['completado'] for p in proyectos if p['etapas']) / max(1, len(proyectos))
        st.metric("Avance General", f"{porcentaje_completado:.0f}%")
    
    # Sección de calendarios
    st.header("📅 Calendarios de Planificación")
    
    tab1, tab2 = st.tabs(["Vista Mensual", "Calendario Interactivo"])
    
    with tab1:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            mes = st.selectbox("Mes", range(1, 13), index=hoy.month-1, key="mes_select")
            año = st.selectbox("Año", range(2023, 2026), index=1, key="año_select")
        
        with col2:
            mostrar_calendario_mensual(proyectos, mes, año)
    
    with tab2:
        mostrar_calendario_interactivo(proyectos)
    
    # Línea de tiempo del proyecto seleccionado
    st.header("⏳ Seguimiento de Proyecto")
    
    if proyectos:
        proyecto_sel = st.selectbox(
            "Seleccionar proyecto para detalles", 
            [p['nombre'] for p in proyectos],
            key="proyecto_sel"
        )
        
        proyecto = next(p for p in proyectos if p['nombre'] == proyecto_sel)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            mostrar_timeline_proyecto(proyecto)
        
        with col2:
            st.subheader("Detalles del Proyecto")
            st.write(f"**Responsable:** {proyecto['responsable']}")
            st.write(f"**Estado:** {proyecto['estado']}")
            st.write(f"**Fecha Inicio:** {proyecto['fecha_inicio'].strftime('%d/%m/%Y')}")
            st.write(f"**Fecha Entrega:** {proyecto['fecha_entrega'].strftime('%d/%m/%Y')}")
            
            dias_restantes = (proyecto['fecha_entrega'] - hoy).days
            if dias_restantes > 0:
                st.metric("Días restantes", dias_restantes)
            else:
                st.metric("Días de retraso", abs(dias_restantes), delta_color="inverse")
            
            # Progreso general del proyecto
            if proyecto.get('etapas'):
                completado = sum(e['completado'] for e in proyecto['etapas']) / len(proyecto['etapas'])
                st.progress(int(completado))
                st.caption(f"Progreso general: {completado:.0f}%")
    else:
        st.warning("No hay proyectos registrados en este departamento")

def gestionar_proyectos_personalizado():
    """Página de gestión completa de proyectos"""
    departamento = st.session_state['departamento']
    usuario_actual = st.session_state['usuario']
    proyectos = cargar_proyectos(departamento)
    
    st.title(f"📋 Gestión de Proyectos - {departamento}")
    
    tab1, tab2, tab3 = st.tabs(["📅 Calendario", "📝 Lista de Proyectos", "➕ Nuevo Proyecto"])
    
    with tab1:
        mostrar_calendario_interactivo(proyectos)
        
        st.subheader("🔔 Próximas Entregas")
        hoy = date.today()
        proximas_entregas = sorted(
            [p for p in proyectos if p['fecha_entrega'] >= hoy],
            key=lambda x: x['fecha_entrega']
        )[:5]
        
        if proximas_entregas:
            for proyecto in proximas_entregas:
                delta = (proyecto['fecha_entrega'] - hoy).days
                estado = proyecto['estado']
                
                if delta <= 7 and estado != "Completado":
                    color = "red"
                elif delta <= 14:
                    color = "orange"
                else:
                    color = "green"
                
                st.markdown(
                    f"""
                    <div style='padding:10px; border-left: 4px solid {color}; margin:5px 0;'>
                        <b>{proyecto['nombre']}</b><br>
                        📅 {proyecto['fecha_entrega'].strftime('%d/%m/%Y')} | 
                        ⏳ {delta} días | 
                        🏷️ {estado}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No hay entregas próximas registradas")
    
    with tab2:
        st.subheader("📋 Todos los Proyectos")
        
        if proyectos:
            df_proyectos = pd.DataFrame(proyectos)
            
            # Filtrar columnas para mostrar
            columnas = ['nombre', 'responsable', 'fecha_inicio', 'fecha_entrega', 'estado']
            st.dataframe(
                df_proyectos[columnas],
                use_container_width=True,
                column_config={
                    "nombre": "Nombre",
                    "responsable": "Responsable",
                    "fecha_inicio": st.column_config.DateColumn("Inicio"),
                    "fecha_entrega": st.column_config.DateColumn("Entrega"),
                    "estado": "Estado"
                }
            )
            
            # Detalles del proyecto seleccionado
            proyecto_sel = st.selectbox(
                "Seleccionar proyecto para editar",
                [p['nombre'] for p in proyectos],
                key="proyecto_editar"
            )
            
            if proyecto_sel:
                # Encontrar el índice del proyecto seleccionado
                proyecto_idx = next(i for i, p in enumerate(proyectos) if p['nombre'] == proyecto_sel)
                proyecto = proyectos[proyecto_idx]
                
                with st.expander(f"✏️ Editar {proyecto_sel}", expanded=True):
                    with st.form(f"form_editar_{proyecto['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nuevo_nombre = st.text_input("Nombre", proyecto['nombre'])
                            nuevo_estado = st.selectbox(
                                "Estado",
                                ["Pendiente", "En progreso", "En revisión", "Completado", "Atrasado"],
                                index=["Pendiente", "En progreso", "En revisión", "Completado", "Atrasado"].index(proyecto['estado'])
                            )
                        
                        with col2:
                            nueva_fecha_inicio = st.date_input("Fecha inicio", proyecto['fecha_inicio'])
                            nueva_fecha_entrega = st.date_input("Fecha entrega", proyecto['fecha_entrega'])
                        
                        if st.form_submit_button("💾 Guardar cambios"):
                            # Actualizar el proyecto en session_state
                            st.session_state.proyectos[departamento][proyecto_idx] = {
                                **proyecto,
                                "nombre": nuevo_nombre,
                                "estado": nuevo_estado,
                                "fecha_inicio": nueva_fecha_inicio,
                                "fecha_entrega": nueva_fecha_entrega
                            }
                            
                            # Verificación de atraso
                            if nueva_fecha_entrega < date.today() and nuevo_estado != "Completado":
                                st.session_state.proyectos[departamento][proyecto_idx]['estado'] = "Atrasado"
                            
                            st.success("Proyecto actualizado correctamente")
                            st.rerun()
        else:
            st.info("No hay proyectos registrados en este departamento")
    
    with tab3:
        st.subheader("🆕 Crear Nuevo Proyecto")
        
        with st.form("form_nuevo_proyecto", clear_on_submit=True):
            nombre = st.text_input("Nombre del proyecto*", placeholder="Ej: Análisis de tendencias 2025")
            
            col1, col2 = st.columns(2)
            with col1:
                fecha_inicio = st.date_input("Fecha de inicio*", date.today())
                responsable = st.selectbox(
                    "Responsable*",
                    [u['nombre'] for u in usuarios[departamento]]
                )
            
            with col2:
                fecha_entrega = st.date_input("Fecha de entrega*", date.today() + timedelta(days=30))
                estado = st.selectbox(
                    "Estado inicial*",
                    ["Pendiente", "En progreso"]
                )
            
            descripcion = st.text_area("Descripción", placeholder="Objetivos y alcance del proyecto...")
            
            # Validaciones
            if fecha_entrega < fecha_inicio:
                st.error("La fecha de entrega no puede ser anterior a la fecha de inicio")
            
            if st.form_submit_button("✅ Crear Proyecto"):
                if not nombre:
                    st.error("El nombre del proyecto es obligatorio")
                else:
                    nuevo_id = max(p['id'] for p in proyectos) + 1 if proyectos else 1
                    
                    nuevo_proyecto = {
                        "id": nuevo_id,
                        "nombre": nombre,
                        "responsable": responsable,
                        "fecha_inicio": fecha_inicio,
                        "fecha_entrega": fecha_entrega,
                        "estado": estado,
                        "descripcion": descripcion,
                        "etapas": []
                    }
                    
                    # Añadir el nuevo proyecto a session_state
                    st.session_state.proyectos[departamento].append(nuevo_proyecto)
                    
                    st.success("Proyecto creado exitosamente!")
                    st.rerun()

# =============================================
# APLICACIÓN PRINCIPAL
# =============================================

def main():
    """Función principal que controla el flujo de la aplicación"""
    if not autenticar_usuario():
        st.warning("Por favor ingrese sus credenciales en la barra lateral")
        return
    
    st.sidebar.title(f"👤 {st.session_state['usuario']}")
    st.sidebar.write(f"**Departamento:** {st.session_state['departamento']}")
    st.sidebar.write(f"**Rol:** {st.session_state['rol']}")
    st.sidebar.divider()
    
    menu = st.sidebar.radio(
        "Menú Principal",
        ["📊 Dashboard", "📋 Proyectos", "📂 Documentos", "📈 Reportes", "⚙️ Configuración"],
        index=0
    )
    
    if menu == "📊 Dashboard":
        mostrar_dashboard_personalizado()
    elif menu == "📋 Proyectos":
        gestionar_proyectos_personalizado()
    elif menu == "📂 Documentos":
        st.title("📂 Gestión Documental")
        st.write("Módulo en desarrollo - Próximamente")
    elif menu == "📈 Reportes":
        st.title("📈 Reportes y Análisis")
        st.write("Módulo en desarrollo - Próximamente")
    elif menu == "⚙️ Configuración":
        st.title("⚙️ Configuración del Usuario")
        st.write("Módulo en desarrollo - Próximamente")

if __name__ == "__main__":
    main()