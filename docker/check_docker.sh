#!/bin/bash

# 🧪 Простая проверка Docker
echo "🔍 Проверка Docker..."

# Проверить запущен ли Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker не запущен!"
    echo "Запустите Docker Desktop и попробуйте снова."
    exit 1
fi

# Показать версию
echo "✅ Docker запущен"
echo "📦 Версия Docker:"
docker --version

# Показать статус контейнеров
echo ""
echo "📊 Статус контейнеров:"
docker ps -a

# Показать версии Docker Compose
echo ""
echo "🐋 Проверка docker-compose..."
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose v1:"
    docker-compose --version
elif command -v docker &> /dev/null; then
    echo "✅ docker compose v2:"
    docker compose version
else
    echo "❌ docker-compose не найден"
fi

# Проверить порт 8081
echo ""
echo "🔍 Проверка порта 8081..."
if command -v netstat &> /dev/null; then
    if netstat -an | grep ":8081.*LISTEN" > /dev/null; then
        echo "✅ Порт 8081 открыт и слушается"
    else
        echo "❌ Порт 8081 не слушается"
    fi
elif command -v ss &> /dev/null; then
    if ss -ltn | grep ":8081" > /dev/null; then
        echo "✅ Порт 8081 открыт и слушается"
    else
        echo "❌ Порт 8081 не слушается"
    fi
else
    echo "⚠️  Не могу проверить порт (netstat/ss не найден)"
fi

echo ""
echo "💡 Попробуйте открыть в браузере: http://localhost:8081"
