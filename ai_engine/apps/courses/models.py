from tortoise import fields, models

class Course(models.Model):
    id = fields.UUIDField(version=7, pk=True)
    owner = fields.ForeignKeyField("models.User", related_name="courses")
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "courses"