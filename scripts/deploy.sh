#!/bin/bash
# Galion Deployment Script
# Deploys entire infrastructure to Kubernetes cluster

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Please install kubectl."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "docker not found. Please install Docker."
        exit 1
    fi
    
    # Check cluster connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster."
        exit 1
    fi
    
    log_info "Prerequisites OK"
}

# Create namespaces
create_namespaces() {
    log_info "Creating namespaces..."
    kubectl apply -f infrastructure/kubernetes/namespaces.yaml
}

# Create secrets
create_secrets() {
    log_info "Creating secrets..."
    
    # Load environment variables
    if [ -f .env ]; then
        source .env
    else
        log_error ".env file not found. Copy env.example to .env and configure it."
        exit 1
    fi
    
    # Database credentials
    kubectl create secret generic db-credentials \
        --from-literal=username="${POSTGRES_USER}" \
        --from-literal=password="${POSTGRES_PASSWORD}" \
        -n galion-data \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Redis credentials
    kubectl create secret generic redis-credentials \
        --from-literal=password="${REDIS_PASSWORD}" \
        -n galion-data \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Velocity secret
    kubectl create secret generic velocity-secret \
        --from-literal=secret="${VELOCITY_SECRET}" \
        -n galion-proxy \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log_info "Secrets created"
}

# Deploy data layer
deploy_data_layer() {
    log_info "Deploying data layer (PostgreSQL, Redis)..."
    
    # PostgreSQL
    kubectl apply -f infrastructure/kubernetes/postgresql/
    
    # Redis
    kubectl apply -f infrastructure/kubernetes/redis/
    
    # Wait for PostgreSQL
    log_info "Waiting for PostgreSQL to be ready..."
    kubectl wait --for=condition=ready pod/postgresql-0 \
        -n galion-data --timeout=300s || true
    
    # Wait for Redis
    log_info "Waiting for Redis to be ready..."
    kubectl wait --for=condition=ready pod -l app=redis \
        -n galion-data --timeout=300s || true
    
    log_info "Data layer deployed"
}

# Deploy proxy layer
deploy_proxy_layer() {
    log_info "Deploying proxy layer (Velocity)..."
    
    kubectl apply -f infrastructure/kubernetes/velocity/
    
    # Wait for Velocity
    log_info "Waiting for Velocity proxies to be ready..."
    kubectl wait --for=condition=ready pod -l app=velocity \
        -n galion-proxy --timeout=300s || true
    
    log_info "Proxy layer deployed"
}

# Deploy server layer
deploy_server_layer() {
    log_info "Deploying server layer (Minecraft servers)..."
    
    kubectl apply -f infrastructure/kubernetes/servers/
    
    log_info "Server layer deployed"
    log_warn "Servers may take 2-5 minutes to fully start"
}

# Deploy monitoring
deploy_monitoring() {
    log_info "Deploying monitoring stack (Prometheus, Grafana)..."
    
    kubectl apply -f infrastructure/kubernetes/monitoring/
    
    log_info "Monitoring deployed"
}

# Get status
get_status() {
    log_info "Deployment status:"
    
    echo ""
    echo "=== Namespaces ==="
    kubectl get namespaces | grep galion
    
    echo ""
    echo "=== Data Layer ==="
    kubectl get pods -n galion-data
    
    echo ""
    echo "=== Proxy Layer ==="
    kubectl get pods -n galion-proxy
    
    echo ""
    echo "=== Server Layer ==="
    kubectl get pods -n galion-servers | head -10
    echo "(Showing first 10 servers...)"
    
    echo ""
    echo "=== Services ==="
    kubectl get svc -n galion-proxy
    
    echo ""
    log_info "Deployment complete!"
    
    # Get external IP
    EXTERNAL_IP=$(kubectl get svc velocity-proxy -n galion-proxy -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    if [ -n "$EXTERNAL_IP" ]; then
        echo ""
        log_info "Connect to server at: ${EXTERNAL_IP}:25565"
    else
        log_warn "External IP not yet assigned. Check status with: kubectl get svc -n galion-proxy"
    fi
}

# Main deployment
main() {
    echo "========================================"
    echo "  Galion Server Deployment"
    echo "  20k Player Infrastructure"
    echo "========================================"
    echo ""
    
    check_prerequisites
    create_namespaces
    create_secrets
    deploy_data_layer
    deploy_proxy_layer
    deploy_server_layer
    deploy_monitoring
    get_status
}

# Run main
main

