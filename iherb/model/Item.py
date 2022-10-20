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
    brand_name = CharField()
    url = CharField()

    # 평점 및 리뷰수 (None 일수도 있음)
    grade = FloatField()
    review = IntegerField()

    # 가격
    price = FloatField()      # 내가 살수 있는 가격
    price_org = FloatField()  # 할인전 가격, 할인 하지 않는다면 price와 동일

    # 할인
    disc_cd = CharField()  # G : 일반 상품 / S : 슈퍼 / P : 특가 / B : 장바구니 할인

    # 이미지
    image_link1 = CharField()
    image_link2 = CharField()
