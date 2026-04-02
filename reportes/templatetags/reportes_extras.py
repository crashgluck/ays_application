from django import template

register = template.Library()


@register.filter
def field_from_name(form, field_name):
    """Permite renderizar form fields dinamicos por nombre en templates."""
    try:
        return form[field_name]
    except Exception:
        return ""
