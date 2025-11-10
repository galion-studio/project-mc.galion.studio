#!/bin/bash
# Galion Scaling Script
# Manually scale server instances

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Display current scale
show_status() {
    echo "Current scaling status:"
    echo ""
    echo "=== Velocity Proxies ==="
    kubectl get deployment velocity-proxy -n galion-proxy
    echo ""
    echo "=== Minecraft Servers ==="
    kubectl get deployment mc-server -n galion-servers
    echo ""
    echo "=== HPA Status ==="
    kubectl get hpa -n galion-proxy
    kubectl get hpa -n galion-servers
}

# Scale proxies
scale_proxies() {
    local replicas=$1
    
    if [ -z "$replicas" ]; then
        log_error "Please specify number of replicas"
        return 1
    fi
    
    log_info "Scaling Velocity proxies to ${replicas} replicas..."
    kubectl scale deployment velocity-proxy --replicas="$replicas" -n galion-proxy
    
    log_info "Waiting for proxies to be ready..."
    kubectl rollout status deployment/velocity-proxy -n galion-proxy
    
    log_info "Proxies scaled successfully"
}

# Scale servers
scale_servers() {
    local replicas=$1
    
    if [ -z "$replicas" ]; then
        log_error "Please specify number of replicas"
        return 1
    fi
    
    # Warn if scaling beyond reasonable limits
    if [ "$replicas" -gt 200 ]; then
        log_warn "Scaling to ${replicas} servers. This will consume significant resources."
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log_info "Scaling cancelled"
            return 0
        fi
    fi
    
    log_info "Scaling Minecraft servers to ${replicas} replicas..."
    kubectl scale deployment mc-server --replicas="$replicas" -n galion-servers
    
    log_info "Scaling in progress... (this may take a few minutes)"
    log_info "Monitor with: kubectl get pods -n galion-servers -w"
}

# Calculate required scale based on player count
calculate_scale() {
    local target_players=$1
    local players_per_server=80  # Conservative estimate
    
    if [ -z "$target_players" ]; then
        log_error "Please specify target player count"
        return 1
    fi
    
    local required_servers=$(( (target_players + players_per_server - 1) / players_per_server ))
    local buffer=$(( required_servers * 20 / 100 ))  # 20% buffer
    local total=$(( required_servers + buffer ))
    
    echo ""
    log_info "Calculation for ${target_players} players:"
    echo "  Players per server: ${players_per_server}"
    echo "  Required servers: ${required_servers}"
    echo "  Buffer (20%): ${buffer}"
    echo "  Recommended total: ${total}"
    echo ""
    
    read -p "Scale to ${total} servers? (yes/no): " confirm
    if [ "$confirm" == "yes" ]; then
        scale_servers "$total"
    fi
}

# Help message
show_help() {
    echo "Galion Scaling Script"
    echo ""
    echo "Usage:"
    echo "  $0 status                      # Show current scaling status"
    echo "  $0 proxies <count>             # Scale Velocity proxies"
    echo "  $0 servers <count>             # Scale Minecraft servers"
    echo "  $0 calculate <player_count>    # Calculate required servers"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 proxies 5"
    echo "  $0 servers 50"
    echo "  $0 calculate 5000"
}

# Main
case "${1:-status}" in
    status)
        show_status
        ;;
    proxies)
        scale_proxies "$2"
        ;;
    servers)
        scale_servers "$2"
        ;;
    calculate)
        calculate_scale "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

