#!/usr/bin/env bash
set -e

mkdir -p config
mkdir -p load_data

if [ ! -f config/categories.json ]; then
    cat > config/categories.json << 'EOF'
{
    "CATEGORIES": {
    },
    "POSITIVE_CATEGORIES": []
}
EOF
fi

echo "Setup complete."
