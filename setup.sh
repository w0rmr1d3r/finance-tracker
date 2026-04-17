#!/usr/bin/env bash
set -e

mkdir -p backend/load/categories
mkdir -p backend/load/entries_files/revolut
mkdir -p backend/load/entries_files/santander
mkdir -p backend/load/entries_files/trading212
mkdir -p backend/saved_files

if [ ! -f backend/load/categories/categories.json ]; then
    cat > backend/load/categories/categories.json << 'EOF'
{
    "CATEGORIES": {
    },
    "POSITIVE_CATEGORIES": []
}
EOF
fi

echo "Setup complete."
