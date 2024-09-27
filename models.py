
from sqlalchemy import ForeignKey, Numeric, String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship

#default= func.now()- це просто поточний час за замовчуванням, який додається тоді коли ми щос додаємо до таблиць 
#onupdate=func.now() - це час яакий буде додаватись тоді, коли ми будемо вносити зміни
class Base(DeclarativeBase):
    created:Mapped[DateTime] = mapped_column(DateTime, default= func.now())
    updated:Mapped[DateTime] = mapped_column(DateTime, default= func.now(), onupdate=func.now())
#primary_key=True- створює індекс для кожного елемента таблиці це для того щоб легше із ним взаємодіяти 
# autoincrement=True- дозволяє створити айді і при додаванні товару у базу даних додасть 1 до поля айді для того щоб воно було унікальним   
#asdecimal - означає що число яке ми будемо вписувати має бути не десятковим 

class Banner(Base):
    __tablename__ = 'banner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), unique=True)
    photo: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Category(Base):
    __tablename__='category'
    
    
    id:Mapped[int]= mapped_column(primary_key=True, autoincrement= True)
    name:Mapped[str]= mapped_column(String(20), nullable=False)    

class Product(Base):
    __tablename__='product'

    id:Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]= mapped_column(String(150), nullable=False)
    description:Mapped[str]= mapped_column(Text)
    price:Mapped[float]= mapped_column(Numeric(asdecimal = True), nullable= False)
    photo:Mapped[str]= mapped_column(String(150))
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id',ondelete = 'CASCADE'), nullable=False)

    category:Mapped['Category'] = relationship(backref = 'product')

    
class User(Base):
    __tablename__='user'

    id:Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int]= mapped_column(unique=True)
    first_name:Mapped[str] = mapped_column(String(150), nullable=True)

    last_name:Mapped[str] = mapped_column(String(150), nullable=True)
    phone:Mapped[str]= mapped_column(String(15), nullable=True)



class Cart(Base):
    __tablename__='cart'
    id:Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user:Mapped['User']= relationship(backref='cart')

    quantity:Mapped[int]

    product_id:Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product:Mapped['Product']= relationship(backref='cart')