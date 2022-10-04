from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField, FixedCharField

from iherb.model.BaseModel import BaseModel


class Item(BaseModel):
    class Meta:
        db_table = 'Item'
        # primary_key
        # indexes = (
        #     (('exchange', 'symbol'), False),
        # )

    id = CharField(primary_key=True)
    title = CharField()
    price = IntegerField()
    quantity = IntegerField()
    care_info = CharField()
    image_url_info = CharField()
