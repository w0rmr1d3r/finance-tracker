#!/usr/bin/env bash
set -e

mkdir -p backend/load/categories
mkdir -p backend/load/entries_files/revolut
mkdir -p backend/load/entries_files/santander
mkdir -p backend/saved_files

cat > backend/load/categories.json << 'EOF'
{
    "CATEGORIES": {
    },
    "POSITIVE_CATEGORIES": []
}
EOF

echo "Setup complete."
