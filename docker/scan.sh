#!/bin/bash

# ═══════════════════════════════════════════════════════════
# 🐳 Запуск SAFEX + Тестовый сервер
# ═══════════════════════════════════════════════════════════

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           🐳 SAFEX + ТЕСТОВЫЙ СЕРВЕР               ║"
    echo "║                                                          ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

# Запустить контейнеры
start_scan() {
    print_header
    echo -e "${BLUE}🚀 Запуск контейнеров...${NC}"
    echo ""
    
    docker-compose -f docker-compose.scan.yml up -d
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Контейнеры запущены!${NC}"
        echo ""
        echo "📦 Контейнеры:"
        echo "   🔴 safex-scanner        - SAFEX (порт 8001)"
        echo "   🎯 test-vulnerable-server - Тестовый сервер (порт 8081)"
        echo "   🐘 safex-test-db         - PostgreSQL (порт 5433)"
        echo "   🔴 safex-test-redis      - Redis (порт 6381)"
        echo ""
        echo "🌐 Доступные URL:"
        echo "   📄 Тестовая страница: http://localhost:8081"
        echo "   🔍 SAFEX API: http://localhost:8001"
        echo "   📊 Отчеты: ./test-reports/"
        echo ""
    else
        echo -e "${RED}❌ Ошибка запуска контейнеров${NC}"
        exit 1
    fi
}

# Сканировать тестовый сервер
scan_target() {
    echo -e "${CYAN}🔍 Сканирование тестового сервера...${NC}"
    echo ""
    
    # Сканировать через SAFEX CLI
    docker exec safex-scanner python safex.py scan test-targets/vulnerable_app.py --language ru
    
    # Сканировать конфиги
    docker exec safex-scanner python safex.py scan test-targets/index.html --language ru
    
    echo ""
    echo -e "${GREEN}✅ Сканирование завершено!${NC}"
    echo ""
}

# Показать отчеты
show_reports() {
    echo -e "${CYAN}📊 Отчеты сканирования:${NC}"
    echo ""
    
    # Найти JSON отчеты
    find test-reports -name "*.json" -type f | while read -r file; do
        echo -e "${YELLOW}📄 $file${NC}"
        # Показать последние 10 строк
        tail -10 "$file"
        echo ""
    done
}

# Остановить контейнеры
stop_scan() {
    echo -e "${YELLOW}⏹  Остановка контейнеров...${NC}"
    echo ""
    
    docker-compose -f docker-compose.scan.yml down
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Контейнеры остановлены${NC}"
        echo ""
    else
        echo -e "${RED}❌ Ошибка остановки${NC}"
        exit 1
    fi
}

# Очистить все
clean_scan() {
    print_header
    echo -e "${RED}🗑️  ОЧИСТКА ВСЕХ КОНТЕЙНЕРОВ И ДАННЫХ!${NC}"
    echo ""
    
    docker-compose -f docker-compose.scan.yml down -v
    
    # Удалить отчеты
    rm -rf test-reports/*
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Все удалено${NC}"
        echo ""
    else
        echo -e "${RED}❌ Ошибка удаления${NC}"
        exit 1
    fi
}

# Показать логи SAFEX
show_logs() {
    echo -e "${CYAN}📝 Логи SAFEX:${NC}"
    echo ""
    
    docker logs -f safex-scanner
}

# Показать статус
show_status() {
    echo -e "${CYAN}📊 Статус контейнеров:${NC}"
    echo ""
    
    docker-compose -f docker-compose.scan.yml ps
    echo ""
}

# Справка
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  up        - Запустить контейнеры"
    echo "  scan      - Запустить SAFEX и сканировать тестовый сервер"
    echo "  reports   - Показать отчеты сканирования"
    echo "  logs      - Показать логи SAFEX"
    echo "  status    - Показать статус контейнеров"
    echo "  stop      - Остановить контейнеры"
    echo "  clean     - 🗑️  Удалить все контейнеры и данные"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 up              # Запустить контейнеры"
    echo "  $0 scan            # Запустить сканирование"
    echo "  $0 reports         # Показать отчеты"
    echo "  $0 clean           # Удалить всё"
    echo ""
}

# Главное меню
main() {
    case "${1:-help}" in
        up)
            start_scan
            ;;
        scan)
            start_scan
            scan_target
            show_reports
            ;;
        reports)
            show_reports
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        stop)
            stop_scan
            ;;
        clean)
            clean_scan
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Неизвестная команда: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Запуск
main "$@"
