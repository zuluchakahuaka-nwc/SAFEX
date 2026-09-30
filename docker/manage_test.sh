#!/bin/bash

# ═════════════════════════════════════════════════════════════
# УПРАВЛЕНИЕ ТЕСТОВОЙ СРЕДОЙ DOCKER
# ═════════════════════════════════════════════════════════════

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[FAIL] $1${NC}"
}

print_header() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║ SAFEX TEST DOCKER MANAGER ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
}

# Показать справку
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  up          - Запустить тестовую среду"
    echo "  down        - Остановить тестовую среду"
    echo "  restart     - Перезапустить тестовую среду"
    echo "  status      - Показать статус контейнеров"
    echo "  logs        - Показать логи всех контейнеров"
    echo "  logs-api    - Показать логи API"
    echo "  logs-db     - Показать логи базы данных"
    echo " clean - [!] УДАЛИТЬ ВСЕ контейнеры и данные!"
    echo " reset - [!] ОСТОРОЖНО: Полный сброс (удаление + пересоздание)"
    echo "  backup      - Создать бэкап тестовых данных"
    echo "  restore     - Восстановить бэкап"
    echo "  help        - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 up              # Запустить тестовую среду"
    echo "  $0 logs            # Просмотреть логи"
    echo "  $0 clean           # Удалить все контейнеры и данные"
    echo ""
}

# Запустить тестовую среду
start_test_env() {
    print_header
    print_info "Запуск тестовой среды..."

    docker-compose -f docker-compose.test.yml up -d

    if [ $? -eq 0 ]; then
        print_success "Тестовая среда запущена!"
        echo ""
        echo " Доступные сервисы:"
        echo "   - API: http://localhost:8001"
        echo "   - API Docs: http://localhost:8001/docs"
        echo "   - База данных: localhost:5433"
        echo "   - Redis: localhost:6380"
        echo "   - Prometheus: http://localhost:9091"
        echo "   - Grafana: http://localhost:3001 (admin/admin_test123)"
        echo ""
        echo " Логи:"
        echo "   $0 logs         # Все логи"
        echo "   $0 logs-api     # Логи API"
        echo "   $0 logs-db      # Логи БД"
        echo ""
    else
        print_error "Ошибка запуска тестовой среды"
        exit 1
    fi
}

# Остановить тестовую среду
stop_test_env() {
    print_info "Остановка тестовой среды..."

    docker-compose -f docker-compose.test.yml down

    if [ $? -eq 0 ]; then
        print_success "Тестовая среда остановлена"
        echo ""
    else
        print_error "Ошибка остановки тестовой среды"
        exit 1
    fi
}

# Перезапустить тестовую среду
restart_test_env() {
    print_info "Перезапуск тестовой среды..."

    docker-compose -f docker-compose.test.yml restart

    if [ $? -eq 0 ]; then
        print_success "Тестовая среда перезапущена"
        echo ""
    else
        print_error "Ошибка перезапуска тестовой среды"
        exit 1
    fi
}

# Показать статус
show_status() {
    print_info "Статус контейнеров:"
    echo ""

    docker-compose -f docker-compose.test.yml ps

    echo ""
    print_info "Использование ресурсов:"
    echo ""
    docker stats --no-stream $(docker-compose -f docker-compose.test.yml ps -q)
    echo ""
}

# Показать логи
show_logs() {
    print_info "Логи всех контейнеров:"
    echo ""

    docker-compose -f docker-compose.test.yml logs -f
}

# Показать логи API
show_logs_api() {
    print_info "Логи API контейнера:"
    echo ""

    docker-compose -f docker-compose.test.yml logs -f safex-api
}

# Показать логи базы данных
show_logs_db() {
    print_info "Логи базы данных:"
    echo ""

    docker-compose -f docker-compose.test.yml logs -f test-db
}

# [!] Очистить (удалить все!)
clean_test_env() {
    print_header
    print_warning "ВНИМАНИЕ! Это удалит ВСЕ тестовые контейнеры и данные!"
    echo ""

    read -p "Вы уверены? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        print_info "Удаление контейнеров и данных..."

        docker-compose -f docker-compose.test.yml down -v

        # Удалить volumes
        docker volume rm safex-test-db-data 2>/dev/null || true
        docker volume rm safex-test-redis-data 2>/dev/null || true
        docker volume rm safex-test-data 2>/dev/null || true
        docker volume rm safex-test-reports 2>/dev/null || true
        docker volume rm safex-test-logs 2>/dev/null || true
        docker volume rm safex-test-nginx-logs 2>/dev/null || true
        docker volume rm safex-test-prometheus-data 2>/dev/null || true
        docker volume rm safex-test-grafana-data 2>/dev/null || true

        # Удалить сеть
        docker network rm safex-test-network 2>/dev/null || true

        print_success "Все контейнеры и данные удалены!"
        echo ""
    else
        print_info "Отменено"
        echo ""
    fi
}

# Полный сброс
reset_test_env() {
    print_header
    print_warning "[!] ОСТОРОЖНО! Полный сброс тестовой среды!"
    print_warning "Это УДАЛИТ все контейнеры, данные и пересоздаст заново!"
    echo ""

    read -p "Вы уверены? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        # Сначала очистить
        clean_test_env

        # Подождать
        sleep 2

        # Пересоздать
        print_info "Пересоздание тестовой среды..."
        docker-compose -f docker-compose.test.yml up -d --force-recreate

        if [ $? -eq 0 ]; then
            print_success "Тестовая среда сброшена и пересоздана!"
            echo ""
        else
            print_error "Ошибка сброса тестовой среды"
            exit 1
        fi
    else
        print_info "Отменено"
        echo ""
    fi
}

# Создать бэкап
backup_test_env() {
    print_header
    print_info "Создание бэкапа тестовых данных..."
    echo ""

    BACKUP_DIR="docker/backups/test"
    BACKUP_NAME="test_backup_$(date +%Y%m%d_%H%M%S)"

    mkdir -p "$BACKUP_DIR"

    # Бэкап volumes
    print_info "Бэкап volumes..."
    docker run --rm \
        -v safex-test-db-data:/db-data \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf "/backup/${BACKUP_NAME}_db.tar.gz" -C /db-data .

    docker run --rm \
        -v safex-test-redis-data:/redis-data \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf "/backup/${BACKUP_NAME}_redis.tar.gz" -C /redis-data .

    print_success "Бэкап создан: $BACKUP_DIR/$BACKUP_NAME"
    echo ""
}

# Восстановить бэкап
restore_test_env() {
    print_header
    print_info "Восстановление бэкапа..."
    echo ""

    BACKUP_DIR="docker/backups/test"

    if [ ! -d "$BACKUP_DIR" ]; then
        print_error "Директория бэкапов не найдена: $BACKUP_DIR"
        exit 1
    fi

    echo "Доступные бэкапы:"
    ls -lh "$BACKUP_DIR" | grep ".tar.gz"

    read -p "Введите имя бэкапа для восстановления: " backup_name

    if [ -f "$BACKUP_DIR/$backup_name" ]; then
        print_info "Восстановление из: $backup_name"

        # Остановить контейнеры
        docker-compose -f docker-compose.test.yml down

        # Восстановить volumes
        if [[ "$backup_name" == *"_db.tar.gz" ]]; then
            docker run --rm \
                -v safex-test-db-data:/db-data \
                -v "$BACKUP_DIR":/backup \
                alpine tar xzf "/backup/$backup_name" -C /db-data
        elif [[ "$backup_name" == *"_redis.tar.gz" ]]; then
            docker run --rm \
                -v safex-test-redis-data:/redis-data \
                -v "$BACKUP_DIR":/backup \
                alpine tar xzf "/backup/$backup_name" -C /redis-data
        fi

        # Запустить контейнеры
        docker-compose -f docker-compose.test.yml up -d

        print_success "Бэкап восстановлен!"
        echo ""
    else
        print_error "Бэкап не найден: $backup_name"
        exit 1
    fi
}

# Главное меню
main() {
    case "${1:-help}" in
        up)
            start_test_env
            ;;
        down)
            stop_test_env
            ;;
        restart)
            restart_test_env
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        logs-api)
            show_logs_api
            ;;
        logs-db)
            show_logs_db
            ;;
        clean)
            clean_test_env
            ;;
        reset)
            reset_test_env
            ;;
        backup)
            backup_test_env
            ;;
        restore)
            restore_test_env
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Неизвестная команда: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Запуск
main "$@"
