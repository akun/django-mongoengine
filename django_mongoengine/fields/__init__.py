from . import djangoflavor

def init_module():
    """
    Create classes with Django-flavor mixins,
    use DjangoField mixin as default
    """
    import sys
    from mongoengine import fields
    current_module = sys.modules[__name__]
    current_module.__all__ = fields.__all__

    for name in fields.__all__:
        fieldcls = getattr(fields, name)
        mixin = getattr(djangoflavor, name, djangoflavor.DjangoField)
        setattr(
            current_module, name,
            type(name, (mixin, fieldcls), {})
        )
init_module()

def patch_mongoengine_fields():
    """
    patch mongoengine.StringField for comparison support
    becouse it's required in django.forms.models.fields_for_model
    importing using mongoengine internal import cache
    """
    from mongoengine import common
    StringField = common._import_class("StringField")
    for k in ["__eq__", "__lt__"]:
        if not k in StringField.__dict__:
            setattr(StringField, k, djangoflavor.DjangoField.__dict__[k])

patch_mongoengine_fields()
