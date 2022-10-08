from peewee import PrimaryKeyField, CharField, IntegerField, FloatField, BooleanField

from iherb.model.BaseModel import BaseModel


class Item(BaseModel):
    class Meta:
        db_table = 'Item'
        # primary_key
        # indexes = (
        #     (('exchange', 'symbol'), False),
        # )

    # 상품 정보
    id = CharField(primary_key=True)
    title = CharField()
    price = IntegerField()
    quantity = IntegerField()
    care_info = CharField()
    image_url_info = CharField()

    # 할인
    super_yn = BooleanField()    # 슈퍼 할인
    super_rate = FloatField()
    basket_yn = BooleanField()   # 장바구니 할인
    basket_rate = FloatField()
    special_yn = BooleanField()  # 특가 할인
