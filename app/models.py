from app.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, Float
from typing import List
from enum import Enum


class RoleEnum(Enum):
    buyer = 'buyer'
    seller = 'seller'
    admin = 'admin'


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Validates
    @validates('role')
    def validate_role(self, key, value):
        if value not in RoleEnum.__members__:
            raise ValueError(f'Invalid role: {value}')
        return value

    # Relationships
    products: Mapped[List["Product"]] = relationship("Product", back_populates="seller", cascade="all, delete")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="buyer", cascade="all, delete")


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationships
    seller: Mapped["User"] = relationship("User", back_populates="products")
    order_products: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")


class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationships
    buyer: Mapped["User"] = relationship("User", back_populates="orders")
    order_products: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order",
                                                             cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="order_products")
    product: Mapped["Product"] = relationship("Product", back_populates="order_products")


