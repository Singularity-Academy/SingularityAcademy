from tortoise import fields, models

class User(models.Model):
    id = fields.BigIntField(pk=True)  # Using BigInt for uint64
    username = fields.CharField(max_length=255, null=False)
    email = fields.CharField(max_length=255, unique=True, null=False)
    password = fields.CharField(max_length=255, null=False)
    is_verified = fields.BooleanField(default=False)
    verification_token = fields.CharField(max_length=10, null=True)
    register_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
