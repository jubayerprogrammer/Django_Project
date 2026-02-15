from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.permission_config import PERMISSION_CONFIG

def assing_permission(user,role):
  
    role_permissions = PERMISSION_CONFIG.get(role,{})
    for model,permission_list in role_permissions.items():
        content_type = ContentType.objects.get_for_model(model)

        for per_codename in permission_list:
            permission_add = Permission.objects.get(
                content_type = content_type,
                codename = f"{per_codename}_{model._meta.model_name}"
            )
            print(permission_add)

            user.user_permissions.add(permission_add)
           