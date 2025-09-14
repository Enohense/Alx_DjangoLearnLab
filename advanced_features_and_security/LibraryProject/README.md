# LibraryProject - Django Introduction
# Permissions & Groups

- Custom permissions are defined on `content.models.Document` with codenames:
  - `can_view`, `can_create`, `can_edit`, `can_delete`.
- Views enforce permissions using `@permission_required("content.<codename>", raise_exception=True)`.

## Groups
Three groups are used:
- **Viewers** → `can_view` (+ builtin `view_document`)
- **Editors** → `can_view`, `can_create`, `can_edit` (+ builtin add/change/view)
- **Admins**  → all custom (`can_*`) + all builtin (add/change/delete/view)

`content.apps.ContentConfig` seeds these groups after `migrate`.  
You can also manage groups/permissions manually in Django Admin.

## Testing
1. Create users (`/admin`) and add them to **Viewers**, **Editors**, or **Admins**.
2. Hit protected views:
   - `/content/list/`   → requires `can_view`
   - `/content/create/` → requires `can_create`
   - `/content/<id>/edit/` → requires `can_edit`
   - `/content/<id>/delete/` (POST) → requires `can_delete`
3. Verify access is allowed/denied according to group.
