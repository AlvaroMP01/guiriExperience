# Integration Documentation (Part 3)

This document details the structure and roles defined for **Part 2** (Experiences, Hotels, and Houses) to facilitate the integration of users and authentication by the rest of the team.

## Defined User Roles

| Role | Description | Permissions in Part 2 |
| :--- | :--- | :--- |
| `CUSTOMER` | End user looking for leisure. | View services and create records in the `reservas` table. |
| `PROVIDER` | Owner of hotels, houses, or a guide. | CRUD of their own services (`experiences`, `hotels`, `houses`). |
| `ADMIN` | Total administrator. | Global management of all services. |

## Data Models (SQLAlchemy)

The following models are defined in `models.py`:
- `Usuario`: (id, nombre, email, password, **rol**)
- `ExperienciaCulinaria`: (id, titulo, descripcion, precio, ubicacion, imagen, **proveedor_id**)
- `Hotel`: (id, nombre, descripcion, estrellas, precio_noche, ubicacion, imagen, **proveedor_id**)
- `CasaAlquiler`: (id, nombre, descripcion, habitaciones, precio_dia, ubicacion, imagen, **proveedor_id**)
- `Reserva`: (id, usuario_id, tipo_servicio, servicio_id, fecha_reserva, fecha_inicio, fecha_fin, total, estado)

## Suggested Integration
- The `rol` field in the `usuarios` table should be used to protect administration routes.
- Service tables have a `ForeignKey` to `usuarios.id` called `proveedor_id`.
- When making a booking, the `current_user.id` should be captured for the `reservas` table.
- **Booking Status**: Defaults to `PENDING`. Can be updated to `CONFIRMED` or `CANCELLED`.

## Implemented Routes (Part 2)
- `/experiences` - GET: List of experiences.
- `/hotels` - GET: List of hotels.
- `/houses` - GET: List of rental houses.
- `/admin/new-service` - GET: Form (logic for saving and auth pending).
