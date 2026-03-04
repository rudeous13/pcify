# GEMINI PROJECT CONTEXT
Project: PCIFY
Type: PC Hardware E-commerce Platform
Backend: Django
Database: MySQL 8.0
Schema Source: pcify.sql
Virtual Environment: [type: Conda, name: pcify]

This file provides architectural context so Gemini can correctly assist development.

------------------------------------------------

# 1 PROJECT PURPOSE

PCIFY is an e-commerce system for selling **PC components and hardware**.

It supports:

• online purchases  
• in-store POS sales  
• supplier procurement  
• warehouse inventory management  
• product compatibility for PC parts  

The system must support both **customers and internal staff operations**.

------------------------------------------------

# 2 DATABASE SOURCE OF TRUTH

The database schema defined in:

pcify.sql

is the authoritative data model.

Gemini must not redesign the schema unless explicitly requested.

When generating Django models, preserve:

• primary keys
• foreign keys
• unique constraints
• check constraints

------------------------------------------------

# 3 CORE DOMAIN MODULES

The schema is divided into logical modules.

### Authentication

Tables

Roles  
Users  
Customers  
Staff  

Rules

Users represent accounts.

A user can be either:

• Customer  
• Staff

Staff members have roles such as:

• AdminStaff
• DeliveryStaff
• SalesStaff

Customers represent purchasing users.

------------------------------------------------

### Product Catalog

Tables

Categories  
Brands  
ComponentTypes  
Products  
ProductVariants  
ProductVariantImages  
ProductReviews  

Products describe hardware items.

Variants represent purchasable SKUs.

Variants contain:

• price
• attributes JSON
• SKU

Reviews belong to variants.

------------------------------------------------

### Location & Addressing

Tables

States  
Cities  
Pincodes  
Addresses  
AddressTypes  
CustomerAddresses  

Customers can have multiple addresses.

Addresses reference pincodes which map to cities and states.

------------------------------------------------

### Shopping Features

Tables

Carts  
CartItems  

Wishlists  
WishlistItems  

Each customer has:

• one cart
• one wishlist

------------------------------------------------

### Order System

Tables

Orders  
OrderItems  
OrderStatuses  
ShippingMethods  
OrderAddresses  

Orders snapshot delivery addresses to maintain history.

OrderItems reference product variants.

------------------------------------------------

### Payments

Tables

Invoices  
Payments  
PaymentMethods  
PaymentStatuses  

Invoices belong to orders.

Payments belong to invoices.

------------------------------------------------

### POS System

Tables

POSTransactions  
POSTransactionItems  

Used for in-store purchases handled by staff.

------------------------------------------------

### Delivery System

Tables

Deliveries  
DeliveryStatuses  
ShipmentPackages  

Deliveries track shipment lifecycle.

Delivery staff may be assigned.

------------------------------------------------

### Procurement

Tables

Suppliers  
PurchaseOrders  
PurchaseOrderItems  
PurchaseOrderStatuses  

Used for restocking inventory from suppliers.

------------------------------------------------

### Inventory Management

Tables

Inventories  
StockReservations  
InventoryTransactions  
TransactionTypes  

Inventories track total and reserved quantities.

StockReservations temporarily reserve stock for orders.

InventoryTransactions record stock movement.

------------------------------------------------

### PC Hardware Components

Tables

CPUs  
RAMs  
Motherboards  
SocketTypes  
ChipsetTypes  
InterfaceTypes  
FormFactors  
RAMTypes  

These tables allow compatibility filtering for PC parts.

------------------------------------------------

# 4 DJANGO IMPLEMENTATION RULES

Gemini must generate Django code following these rules.

Use a **custom User model**.

Use `AbstractUser` or `AbstractBaseUser`.

Authentication should use:

email login  
secure password hashing  

------------------------------------------------

# 5 DJANGO APP STRUCTURE

Recommended Django apps:

accounts
catalog
cart
orders
payments
delivery
inventory
procurement
hardware

------------------------------------------------

# 6 TEMPLATE STRUCTURE

Existing HTML files should become Django templates.

templates/
    base.html
    home.html
    product_list.html
    product_detail.html
    cart.html
    checkout.html

Static files:

static/
    css/
    js/
    images/

------------------------------------------------

# 7 BUSINESS LOGIC RULES

Gemini must respect these behaviors.

CartItems store the price snapshot when added.

OrderItems store the price at purchase time.

OrderAddresses snapshot delivery details.

Inventory reservations prevent overselling.

------------------------------------------------

# 8 DEVELOPMENT PRIORITY

Feature implementation order

1 Authentication
2 Product catalog
3 Cart system
4 Checkout
5 Orders
6 Payments
7 Delivery
8 Inventory
9 Supplier procurement
10 POS

------------------------------------------------

# 9 AI ASSISTANCE RULES

When Gemini answers questions it should:

• reference the SQL schema  
• maintain relational integrity  
• generate Django-friendly implementations  
• explain design choices clearly  

If a request conflicts with the schema, Gemini should explain why.

------------------------------------------------

END OF CONTEXT