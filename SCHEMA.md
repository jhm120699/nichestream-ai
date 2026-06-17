# NicheStream AI - Database Schema

This schema stores product information, features, and AI-generated reviews for programmatic publishing.

## Tables

### `products`
Stores the core product details.
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `name`: TEXT NOT NULL
- `category`: TEXT NOT NULL
- `brand`: TEXT
- `description`: TEXT
- `affiliate_url`: TEXT
- `created_at`: DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at`: DATETIME DEFAULT CURRENT_TIMESTAMP

### `product_features`
Stores specific features for each product.
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `product_id`: INTEGER NOT NULL, FOREIGN KEY REFERENCES `products(id)`
- `feature_name`: TEXT NOT NULL
- `feature_value`: TEXT NOT NULL

### `product_pros`
Stores pros for each product.
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `product_id`: INTEGER NOT NULL, FOREIGN KEY REFERENCES `products(id)`
- `pro_text`: TEXT NOT NULL

### `product_cons`
Stores cons for each product.
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `product_id`: INTEGER NOT NULL, FOREIGN KEY REFERENCES `products(id)`
- `con_text`: TEXT NOT NULL

### `reviews`
Stores the AI-generated review content and metadata.
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `product_id`: INTEGER NOT NULL, FOREIGN KEY REFERENCES `products(id)`
- `title`: TEXT NOT NULL
- `content`: TEXT NOT NULL (Markdown)
- `rating`: REAL
- `status`: TEXT DEFAULT 'draft' (draft, published)
- `slug`: TEXT UNIQUE NOT NULL
- `seo_title`: TEXT
- `seo_description`: TEXT
- `published_at`: DATETIME
- `created_at`: DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at`: DATETIME DEFAULT CURRENT_TIMESTAMP
