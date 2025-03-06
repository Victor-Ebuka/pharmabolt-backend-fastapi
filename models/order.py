from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base


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
    drugs = relationship("DrugOrder", back_populates="order")