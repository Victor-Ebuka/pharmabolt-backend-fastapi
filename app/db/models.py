from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from app.db.base import Base

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_no = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False, default="user")
    refresh_token = Column(Text, unique=True)

    prescriptions = relationship("Prescription", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    prescription_date = Column(Date, nullable=False)
    instructions = Column(Text)

    user = relationship("User", back_populates="prescriptions")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_price = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)


order_no_seq = Sequence('order_no_seq', start=11111111)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date)
    payment_method = Column(String(255), nullable=False)
    delivery_method = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_total = Column(Integer, nullable=False)
    delivery_fee = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    delivery_address = Column(String(255), nullable=False)
    order_no = Column(Integer, order_no_seq, server_default=order_no_seq.next_value(), unique=True, nullable=False)

    user = relationship("User", back_populates="orders")


class MailingList(Base):
    __tablename__ = "mailing_list"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)


class DrugCart(Base):
    __tablename__ = "drugs_carts"

    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), primary_key=True)


class DrugCategory(Base):
    __tablename__ = "drugs_categories"

    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)


class DrugPrescription(Base):
    __tablename__ = "drugs_prescriptions"

    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), primary_key=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False)


class DrugOrder(Base):
    __tablename__ = "drugs_orders"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False)