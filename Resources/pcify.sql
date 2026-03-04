SET default_storage_engine=INNODB;

-- =========================
-- 1. USERS & AUTHENTICATION
-- =========================

CREATE TABLE Roles (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(150) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  role_id INT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE RESTRICT
);

-- =========================
-- 2. CATALOG & PRODUCTS
-- =========================

CREATE TABLE Categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Brands (
  brand_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE ComponentTypes (
  component_type_id INT AUTO_INCREMENT PRIMARY KEY,
  component_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  category_id INT NOT NULL,
  brand_id INT NOT NULL,
  component_type_id INT NOT NULL,
  warranty_months INT DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE RESTRICT,
  FOREIGN KEY (brand_id) REFERENCES Brands(brand_id) ON DELETE RESTRICT,
  FOREIGN KEY (component_type_id) REFERENCES ComponentTypes(component_type_id) ON DELETE RESTRICT
);

CREATE TABLE ProductVariants (
  variant_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  sku VARCHAR(100) NOT NULL UNIQUE,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  attributes JSON,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE ProductVariantImages (
  variant_image_id INT AUTO_INCREMENT PRIMARY KEY,
  variant_id INT NOT NULL,
  image_url VARCHAR(255) NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT FALSE,
  display_order INT DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE CASCADE
);

CREATE TABLE ProductReviews (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  variant_id INT NOT NULL,
  customer_id INT NOT NULL,
  rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE CASCADE,

  FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
    ON DELETE CASCADE,

  UNIQUE (variant_id, customer_id)
);

-- =========================
-- 3. LOCATION & ADDRESSES
-- =========================

CREATE TABLE States (
  state_id INT AUTO_INCREMENT PRIMARY KEY,
  state_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Cities (
  city_id INT AUTO_INCREMENT PRIMARY KEY,
  city_name VARCHAR(100) NOT NULL,
  state_id INT NOT NULL,
  UNIQUE (city_name, state_id),
  FOREIGN KEY (state_id) REFERENCES States(state_id) ON DELETE RESTRICT
);

CREATE TABLE Pincodes (
  pincode_id INT AUTO_INCREMENT PRIMARY KEY,
  pincode VARCHAR(15) UNIQUE NOT NULL,
  city_id INT NOT NULL,
  region_name VARCHAR(100),
  FOREIGN KEY (city_id) REFERENCES Cities(city_id) ON DELETE RESTRICT
);

CREATE TABLE Addresses (
  address_id INT AUTO_INCREMENT PRIMARY KEY,
  street VARCHAR(255) NOT NULL,
  pincode_id INT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (pincode_id) REFERENCES Pincodes(pincode_id) ON DELETE RESTRICT
);

CREATE TABLE AddressTypes (
  address_type_id INT AUTO_INCREMENT PRIMARY KEY,
  address_type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE CustomerAddresses (
  customer_address_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  address_id INT NOT NULL,
  address_type_id INT NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (customer_id, address_id),
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
  FOREIGN KEY (address_id) REFERENCES Addresses(address_id) ON DELETE RESTRICT,
  FOREIGN KEY (address_type_id) REFERENCES AddressTypes(address_type_id) ON DELETE RESTRICT
);

-- =========================
-- 4. SHOPPING CART
-- =========================


CREATE TABLE Carts (
  cart_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (customer_id),
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE CartItems (
  cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
  cart_id INT NOT NULL,
  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (cart_id, variant_id),
  FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE RESTRICT
);

-- =========================
-- 5. WISHLIST
-- =========================

CREATE TABLE Wishlists (
  wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
    ON DELETE CASCADE
);

CREATE TABLE WishlistItems (
  wishlist_item_id INT AUTO_INCREMENT PRIMARY KEY,
  wishlist_id INT NOT NULL,
  variant_id INT NOT NULL,
  added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  UNIQUE (wishlist_id, variant_id),

  FOREIGN KEY (wishlist_id)
    REFERENCES Wishlists(wishlist_id)
    ON DELETE CASCADE,

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE CASCADE
);

-- =========================
-- 6. ORDERS
-- =========================

CREATE TABLE OrderStatuses (
  order_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE ShippingMethods (
  shipping_method_id INT AUTO_INCREMENT PRIMARY KEY,
  method_name VARCHAR(50) UNIQUE NOT NULL,
  delivery_charge DECIMAL(10,2) DEFAULT 0 CHECK (delivery_charge >= 0),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE OrderAddresses (
  order_address_id INT AUTO_INCREMENT PRIMARY KEY,
  street VARCHAR(255) NOT NULL,
  city_name VARCHAR(100) NOT NULL,
  state_name VARCHAR(100) NOT NULL,
  pincode VARCHAR(15) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  -- The address for the order is snapshotted for historical accuracy.
  order_address_id INT NOT NULL,
  order_status_id INT NOT NULL,
  shipping_method_id INT,
  total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
  placed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE RESTRICT,
  FOREIGN KEY (order_address_id) REFERENCES OrderAddresses(order_address_id) ON DELETE RESTRICT,
  FOREIGN KEY (order_status_id) REFERENCES OrderStatuses(order_status_id) ON DELETE RESTRICT,
  FOREIGN KEY (shipping_method_id) REFERENCES ShippingMethods(shipping_method_id) ON DELETE SET NULL
);


CREATE TABLE OrderItems (
  order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (order_id, variant_id),
  FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE RESTRICT
);

-- =========================
-- 7. PAYMENTS & BILLING
-- =========================

CREATE TABLE PaymentStatuses (
  payment_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE PaymentMethods (
  payment_method_id INT AUTO_INCREMENT PRIMARY KEY,
  method_name VARCHAR(50) UNIQUE NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Invoices (
  invoice_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL UNIQUE,
  issued_at TIMESTAMP NOT NULL,
  due_at TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE RESTRICT
);

CREATE TABLE Payments (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  invoice_id INT NOT NULL,
  payment_method_id INT NOT NULL,
  payment_status_id INT NOT NULL,
  transaction_reference VARCHAR(150),
  amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),
  paid_at TIMESTAMP,
  FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) ON DELETE RESTRICT,
  FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(payment_method_id) ON DELETE RESTRICT,
  FOREIGN KEY (payment_status_id) REFERENCES PaymentStatuses(payment_status_id) ON DELETE RESTRICT
);



-- =========================
-- 8. POINT OF SALE (POS)
-- =========================

CREATE TABLE POSTransactions (
  pos_transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  staff_id INT NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
  payment_method_id INT NOT NULL,
  payment_status_id INT NOT NULL,
  transaction_time TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE RESTRICT,
  FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(payment_method_id) ON DELETE RESTRICT,
  FOREIGN KEY (payment_status_id) REFERENCES PaymentStatuses(payment_status_id) ON DELETE RESTRICT
);

CREATE TABLE POSTransactionItems (
  pos_transaction_item_id INT AUTO_INCREMENT PRIMARY KEY,
  pos_transaction_id INT NOT NULL,
  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (pos_transaction_id, variant_id),
  FOREIGN KEY (pos_transaction_id) REFERENCES POSTransactions(pos_transaction_id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE RESTRICT
);

-- =========================
-- 9. DELIVERY & SHIPMENTS
-- =========================

CREATE TABLE DeliveryStatuses (
  delivery_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Deliveries (
  delivery_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  tracking_number VARCHAR(100) UNIQUE,
  delivery_status_id INT NOT NULL,
  staff_id INT,
  shipped_at TIMESTAMP,
  delivered_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (delivery_status_id) REFERENCES DeliveryStatuses(delivery_status_id) ON DELETE RESTRICT,
  FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL
);

CREATE TABLE ShipmentPackages (
  shipment_package_id INT AUTO_INCREMENT PRIMARY KEY,
  delivery_id INT NOT NULL,
  package_number INT NOT NULL,
  weight_kg DECIMAL(8,2),
  length_cm DECIMAL(8,2),
  width_cm DECIMAL(8,2),
  height_cm DECIMAL(8,2),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (delivery_id, package_number),
  FOREIGN KEY (delivery_id) REFERENCES Deliveries(delivery_id) ON DELETE CASCADE
);

-- ==============================
-- 10. SUPPLIERS & PROCUREMENT
-- ==============================

CREATE TABLE Suppliers (
  supplier_id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_name VARCHAR(150) NOT NULL UNIQUE,
  contact_name VARCHAR(100),
  phone_number VARCHAR(20),
  email VARCHAR(150),
  gst_number VARCHAR(20),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE PurchaseOrderStatuses (
  purchase_order_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE PurchaseOrders (
  purchase_order_id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_id INT NOT NULL,
  staff_id INT NOT NULL,
  purchase_order_status_id INT NOT NULL,
  order_date TIMESTAMP NOT NULL,
  expected_delivery TIMESTAMP,
  remarks TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE RESTRICT,
  FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE RESTRICT,
  FOREIGN KEY (purchase_order_status_id) REFERENCES PurchaseOrderStatuses(purchase_order_status_id) ON DELETE RESTRICT
);

CREATE TABLE PurchaseOrderItems (
  purchase_order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  purchase_order_id INT NOT NULL,
  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  received_quantity INT DEFAULT 0 CHECK (received_quantity >= 0),
  CHECK (received_quantity <= quantity),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (purchase_order_id, variant_id),
  FOREIGN KEY (purchase_order_id) REFERENCES PurchaseOrders(purchase_order_id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE RESTRICT
);

-- =========================
-- 11. INVENTORY & STOCK
-- =========================

CREATE TABLE Inventories (
  variant_id INT PRIMARY KEY,
  total_quantity INT NOT NULL DEFAULT 0,
  reserved_quantity INT NOT NULL DEFAULT 0,
  last_updated TIMESTAMP NOT NULL 
    DEFAULT CURRENT_TIMESTAMP 
    ON UPDATE CURRENT_TIMESTAMP,

  CHECK (total_quantity >= 0),
  CHECK (reserved_quantity >= 0),

  CHECK (reserved_quantity <= total_quantity),

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE CASCADE
);

CREATE TABLE TransactionTypes (
  transaction_type_id INT AUTO_INCREMENT PRIMARY KEY,
  type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE StockReservations (
  reservation_id INT AUTO_INCREMENT PRIMARY KEY,
  variant_id INT NOT NULL,
  order_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  UNIQUE (order_id, variant_id),

  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE CASCADE,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);

CREATE TABLE InventoryTransactions (
  inventory_transaction_id INT AUTO_INCREMENT PRIMARY KEY,

  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity <> 0),

  transaction_type_id INT NOT NULL,
  staff_id INT,

  reference_type VARCHAR(50) NOT NULL,
  reference_id INT NOT NULL,

  remarks TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (transaction_type_id)
    REFERENCES TransactionTypes(transaction_type_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (staff_id)
    REFERENCES Staff(staff_id)
    ON DELETE SET NULL
);

-- ====================================
-- 12. PC COMPONENTS & COMPATIBILITY
-- ====================================



CREATE TABLE SocketTypes (
  socket_type_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE ChipsetTypes (
  chipset_type_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE CPUs (
  cpu_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  socket_type_id INT,
  cores INT,
  threads INT,
  base_clock DECIMAL(4,2),
  boost_clock DECIMAL(4,2),
  tdp INT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (socket_type_id) REFERENCES SocketTypes(socket_type_id) ON DELETE SET NULL
);

CREATE TABLE InterfaceTypes (
  interface_type_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE FormFactors (
  form_factor_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE RAMTypes (
  ram_type_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE RAMs (
  ram_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  ram_type_id INT,
  memory_size INT,
  memory_speed INT,
  module_count INT,
  tdp INT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (ram_type_id) REFERENCES RAMTypes(ram_type_id) ON DELETE SET NULL
);

CREATE TABLE Motherboards (
  motherboard_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  socket_type_id INT,
  ram_type_id INT,
  form_factor_id INT,
  chipset_type_id INT,
  max_ram_slots INT,
  max_ram_capacity INT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (socket_type_id) REFERENCES SocketTypes(socket_type_id) ON DELETE SET NULL,
  FOREIGN KEY (ram_type_id) REFERENCES RAMTypes(ram_type_id) ON DELETE SET NULL,
  FOREIGN KEY (form_factor_id) REFERENCES FormFactors(form_factor_id) ON DELETE SET NULL,
  FOREIGN KEY (chipset_type_id) REFERENCES ChipsetTypes(chipset_type_id) ON DELETE SET NULL
);

CREATE TABLE MotherboardInterfaces (
  motherboard_id INT NOT NULL,
  interface_type_id INT NOT NULL,
  supported_slots INT DEFAULT 1, -- optional (e.g., 4 SATA ports)

  PRIMARY KEY (motherboard_id, interface_type_id),

  FOREIGN KEY (motherboard_id)
    REFERENCES Motherboards(motherboard_id)
    ON DELETE CASCADE,

  FOREIGN KEY (interface_type_id)
    REFERENCES InterfaceTypes(interface_type_id)
    ON DELETE RESTRICT
);

CREATE TABLE StorageTypes (
  storage_type_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Storages (
  storage_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  storage_type_id INT NOT NULL,
  capacity_gb INT NOT NULL,
  interface_type_id INT,
  form_factor VARCHAR(50),

  FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
    ON DELETE CASCADE,

  FOREIGN KEY (storage_type_id)
    REFERENCES StorageTypes(storage_type_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (interface_type_id)
    REFERENCES InterfaceTypes(interface_type_id)
    ON DELETE SET NULL
);

CREATE TABLE GPUs (
  gpu_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  memory_size INT,
  length_mm INT NOT NULL,
  interface_type_id INT,
  tdp INT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (interface_type_id) REFERENCES InterfaceTypes(interface_type_id) ON DELETE SET NULL
);

CREATE TABLE PSUs (
  psu_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  wattage INT,
  form_factor_id INT,
  is_modular BOOLEAN,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (form_factor_id) REFERENCES FormFactors(form_factor_id) ON DELETE SET NULL
);

CREATE TABLE Cabinets (
  cabinet_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  max_gpu_length INT,
  max_cooler_height INT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE CabinetFormFactors (
  cabinet_id INT NOT NULL,
  form_factor_id INT NOT NULL,
  PRIMARY KEY (cabinet_id, form_factor_id),
  FOREIGN KEY (cabinet_id) REFERENCES Cabinets(cabinet_id) ON DELETE CASCADE,
  FOREIGN KEY (form_factor_id) REFERENCES FormFactors(form_factor_id) ON DELETE RESTRICT
);

CREATE TABLE CPU_Motherboard_Compatibilities (
  compatibility_id INT AUTO_INCREMENT PRIMARY KEY,
  cpu_id INT NOT NULL,
  motherboard_id INT NOT NULL,
  is_compatible BOOLEAN DEFAULT TRUE,
  notes VARCHAR(255),
  UNIQUE (cpu_id, motherboard_id),
  FOREIGN KEY (cpu_id) REFERENCES CPUs(cpu_id) ON DELETE CASCADE,
  FOREIGN KEY (motherboard_id) REFERENCES Motherboards(motherboard_id) ON DELETE CASCADE
);

CREATE TABLE RAM_Motherboard_Compatibilities (
  compatibility_id INT AUTO_INCREMENT PRIMARY KEY,
  ram_id INT NOT NULL,
  motherboard_id INT NOT NULL,
  max_supported_speed INT,
  max_supported_size INT,
  is_compatible BOOLEAN DEFAULT TRUE,
  UNIQUE (ram_id, motherboard_id),
  FOREIGN KEY (ram_id) REFERENCES RAMs(ram_id) ON DELETE CASCADE,
  FOREIGN KEY (motherboard_id) REFERENCES Motherboards(motherboard_id) ON DELETE CASCADE
);

-- =========================
-- 13. TAXES
-- =========================

CREATE TABLE Taxes (
  tax_id INT AUTO_INCREMENT PRIMARY KEY,
  tax_name VARCHAR(100) NOT NULL UNIQUE,
  tax_rate DECIMAL(5,2) NOT NULL CHECK (tax_rate >= 0),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE OrderItemTaxes (
  order_item_tax_id INT AUTO_INCREMENT PRIMARY KEY,
  order_item_id INT NOT NULL,
  tax_id INT NOT NULL,
  tax_amount DECIMAL(10,2) NOT NULL CHECK (tax_amount >= 0),
  UNIQUE (order_item_id, tax_id),
  FOREIGN KEY (order_item_id) REFERENCES OrderItems(order_item_id) ON DELETE CASCADE,
  FOREIGN KEY (tax_id) REFERENCES Taxes(tax_id) ON DELETE RESTRICT
);

-- =========================
-- 14. RETURNS & REFUNDS
-- =========================


CREATE TABLE ReturnStatuses (
  return_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE ReturnRequests (
  return_request_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  return_status_id INT NOT NULL,
  requested_at TIMESTAMP NOT NULL,
  approved_at TIMESTAMP,
  completed_at TIMESTAMP,
  remarks TEXT,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (return_status_id) REFERENCES ReturnStatuses(return_status_id) ON DELETE RESTRICT
);

CREATE TABLE ReturnItems (
  return_item_id INT AUTO_INCREMENT PRIMARY KEY,
  return_request_id INT NOT NULL,
  order_item_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  reason VARCHAR(255),
  is_restocked BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (return_request_id, order_item_id),
  FOREIGN KEY (return_request_id) REFERENCES ReturnRequests(return_request_id) ON DELETE CASCADE,
  FOREIGN KEY (order_item_id) REFERENCES OrderItems(order_item_id) ON DELETE RESTRICT
);

CREATE TABLE RefundStatuses (
  refund_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Refunds (
  refund_id INT AUTO_INCREMENT PRIMARY KEY,
  return_request_id INT NOT NULL UNIQUE,
  refund_amount DECIMAL(10,2) NOT NULL CHECK (refund_amount >= 0),
  refund_status_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP,
  FOREIGN KEY (return_request_id) REFERENCES ReturnRequests(return_request_id) ON DELETE RESTRICT,
  FOREIGN KEY (refund_status_id) REFERENCES RefundStatuses(refund_status_id) ON DELETE RESTRICT
);


CREATE TABLE RefundPayments (
  refund_payment_id INT AUTO_INCREMENT PRIMARY KEY,
  refund_id INT NOT NULL,
  payment_method_id INT NOT NULL,
  transaction_reference VARCHAR(150),
  amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),
  paid_at TIMESTAMP,
  FOREIGN KEY (refund_id) REFERENCES Refunds(refund_id) ON DELETE RESTRICT,
  FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(payment_method_id) ON DELETE RESTRICT
);

-- =========================
-- 15. SERVICE MODULE
-- =========================

CREATE TABLE Services (
  service_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  description TEXT,
  base_price DECIMAL(10,2) NOT NULL CHECK (base_price >= 0),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE ServiceStatuses (
  service_status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE ServiceRequests (
  service_request_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  service_status_id INT NOT NULL,
  assigned_staff_id INT,
  problem_description TEXT NOT NULL,
  total_amount DECIMAL(10,2) CHECK (total_amount >= 0),
  requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,

  FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (service_status_id)
    REFERENCES ServiceStatuses(service_status_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (assigned_staff_id)
    REFERENCES Staff(staff_id)
    ON DELETE SET NULL
);

CREATE TABLE ServiceRequestItems (
  service_request_item_id INT AUTO_INCREMENT PRIMARY KEY,
  service_request_id INT NOT NULL,
  service_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),

  UNIQUE (service_request_id, service_id),

  FOREIGN KEY (service_request_id)
    REFERENCES ServiceRequests(service_request_id)
    ON DELETE CASCADE,

  FOREIGN KEY (service_id)
    REFERENCES Services(service_id)
    ON DELETE RESTRICT
);

-- OPTIONAL

CREATE TABLE ServicePartsUsed ( 
  service_part_used_id INT AUTO_INCREMENT PRIMARY KEY,
  service_request_id INT NOT NULL,
  variant_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),

  FOREIGN KEY (service_request_id)
    REFERENCES ServiceRequests(service_request_id)
    ON DELETE CASCADE,

  UNIQUE (service_request_id, variant_id),

  FOREIGN KEY (variant_id)
    REFERENCES ProductVariants(variant_id)
    ON DELETE RESTRICT
);

CREATE TABLE ServicePayments (
  service_payment_id INT AUTO_INCREMENT PRIMARY KEY,
  service_request_id INT NOT NULL,
  payment_method_id INT NOT NULL,
  amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),
  paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (service_request_id)
    REFERENCES ServiceRequests(service_request_id)
    ON DELETE RESTRICT,

  FOREIGN KEY (payment_method_id)
    REFERENCES PaymentMethods(payment_method_id)
    ON DELETE RESTRICT
);

-- =========================
-- 16. PC BUILDER
-- =========================

CREATE TABLE PCBuilds (
  build_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  name VARCHAR(150),
  total_price_snapshot DECIMAL(10,2) CHECK (total_price_snapshot >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE PCBuildItems (
  build_item_id INT AUTO_INCREMENT PRIMARY KEY,
  build_id INT NOT NULL,
  variant_id INT NOT NULL,
  price_snapshot DECIMAL(10,2) CHECK (price_snapshot >= 0),
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity >= 1),

  UNIQUE (build_id, variant_id),

  FOREIGN KEY (build_id) REFERENCES PCBuilds(build_id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE RESTRICT
);