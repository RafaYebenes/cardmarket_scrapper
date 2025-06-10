-- Tabla de usuarios
create table users (
    id uuid primary key default gen_random_uuid(),
    telegram_id bigint not null unique,
    username text,
    created_at timestamp with time zone default now()
);

-- Tabla de cartas
create table cards (
    id uuid primary key default gen_random_uuid(),
    code text not null,
    name text not null,
    rarity text,
    language text,
    version_url text,
    last_price numeric(6,2),
    last_update timestamp with time zone,
    unique (code, language, version_url)
);

-- Tabla de seguimientos
create table follows (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references users(id) on delete cascade,
    alert_type text check (alert_type in ('min', 'max', 'both')),
    target_price numeric(6,2) not null,
    min_quantity integer default 1,
    min_condition text, -- Ej: NM, EX, etc.
    last_alert_sent timestamp with time zone,
    created_at timestamp with time zone default now(),
    unique (user_id, alert_type)
);

-- Tabla de historial de precios (opcional)
create table price_history (
    id uuid primary key default gen_random_uuid(),
    card_id uuid references cards(id) on delete cascade,
    price numeric(6,2) not null,
    timestamp timestamp with time zone default now()
);
