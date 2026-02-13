# Documentación para Integración (Parte 3)

Este documento detalla la estructura y los roles definidos para la **Segunda Parte** (Experiencias, Hoteles y Casas) para facilitar la integración de usuarios y autenticación.

## Roles de Usuario Definidos

| Rol | Descripción | Permisos en Parte 2 |
| :--- | :--- | :--- |
| `CLIENTE` | Usuario final que busca ocio. | Visualizar servicios y crear registros en tabla `reservas`. |
| `PROVEEDOR` | Dueño de hoteles, casas o guía. | CRUD de sus propios servicios (`experiencias`, `hoteles`, `casas`). |
| `ADMIN` | Administrador total. | Gestión global de todos los servicios. |

## Modelos de Datos (SQLAlchemy)

Se han definido los siguientes modelos en `models.py`:
- `Usuario`: (id, nombre, email, password, **rol**)
- `ExperienciaCulinaria`: (id, titulo, descripcion, precio, ubicacion, imagen, **proveedor_id**)
- `Hotel`: (id, nombre, descripcion, estrellas, precio_noche, ubicacion, imagen, **proveedor_id**)
- `CasaAlquiler`: (id, nombre, descripcion, habitaciones, precio_dia, ubicacion, imagen, **proveedor_id**)
- `Reserva`: (id, usuario_id, tipo_servicio, servicio_id, fecha_reserva, fecha_inicio, fecha_fin, total, estado)

## Integración sugerida
- El campo `rol` en la tabla `usuarios` debe usarse para proteger las rutas de administración.
- Las tablas de servicios tienen una `ForeignKey` a `usuarios.id` llamada `proveedor_id`.
- Al realizar una reserva, se debe capturar el `current_user.id` para la tabla `reservas`.

## Rutas implementadas (Parte 2)
- `/experiencias` - GET: Listado de experiencias.
- `/hoteles` - GET: Listado de hoteles.
- `/casas` - GET: Listado de casas rurales.
- `/admin/nuevo-servicio` - GET: Formulario (pendiente de lógica de guardado y auth).
