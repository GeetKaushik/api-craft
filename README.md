# APICraft
┌───────────────────────┐
│       React           │
│       Frontend        │
└───────────┬───────────┘
            │
            │ DELETE /users/5
            ↓
┌───────────────────────┐
│       Router          │
│      users.py         │
│                       │
│ HTTP responsibilities │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│       Service         │
│  user_service.py     │
│                       │
│ Business logic        │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│       Session         │
│      SQLModel         │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│      SQLite DB        │
│      apicraft.db      │
└───────────────────────┘