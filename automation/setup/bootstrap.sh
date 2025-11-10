#!/bin/bash
# Titan Server - Bootstrap Script
# One-command setup for development environment
#
# Usage: ./automation/setup/bootstrap.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "  $1"
    echo "========================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main bootstrap process
main() {
    print_header "TITAN SERVER - Bootstrap"
    echo ""
    
    # Check prerequisites
    print_info "Checking prerequisites..."
    
    # Check Docker
    if command_exists docker; then
        print_success "Docker is installed: $(docker --version)"
    else
        print_error "Docker is not installed!"
        echo "Please install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check Docker Compose
    if command_exists docker-compose || docker compose version >/dev/null 2>&1; then
        print_success "Docker Compose is installed"
    else
        print_error "Docker Compose is not installed!"
        echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # Check Java (optional, for building)
    if command_exists java; then
        JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
        print_success "Java is installed: $JAVA_VERSION"
    else
        print_warning "Java not found (needed for building from source)"
        print_info "You can still run using Docker"
    fi
    
    echo ""
    print_header "Setting up environment"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "Please edit .env file with your configuration!"
    else
        print_info ".env file already exists"
    fi
    
    # Create required directories
    print_info "Creating directory structure..."
    mkdir -p worlds/hub worlds/survival worlds/creative
    mkdir -p logs backups plugins mods config
    mkdir -p monitoring/grafana/dashboards
    mkdir -p automation/backup automation/deploy
    print_success "Directories created"
    
    # Create .gitkeep files for empty directories
    touch worlds/.gitkeep
    touch logs/.gitkeep
    touch backups/.gitkeep
    
    # Set permissions for scripts
    print_info "Setting script permissions..."
    find automation -type f -name "*.sh" -exec chmod +x {} \;
    print_success "Scripts are now executable"
    
    echo ""
    print_header "Building Project"
    
    # Build with Gradle if Java is available
    if command_exists java && [ -f gradlew ]; then
        print_info "Building project with Gradle..."
        ./gradlew clean build -x test
        print_success "Build completed"
    else
        print_warning "Skipping Gradle build (Java not available or gradlew not found)"
        print_info "Will use Docker to build instead"
    fi
    
    echo ""
    print_header "Docker Setup"
    
    # Pull base images
    print_info "Pulling required Docker images..."
    docker pull eclipse-temurin:17-jre-alpine || print_warning "Failed to pull Java image"
    docker pull postgres:15-alpine || print_warning "Failed to pull PostgreSQL image"
    docker pull redis:7-alpine || print_warning "Failed to pull Redis image"
    docker pull prom/prometheus:latest || print_warning "Failed to pull Prometheus image"
    docker pull grafana/grafana:latest || print_warning "Failed to pull Grafana image"
    
    echo ""
    print_header "Starting Services"
    
    # Start Docker Compose
    print_info "Starting Titan services with Docker Compose..."
    docker-compose up -d
    
    echo ""
    print_info "Waiting for services to be ready..."
    sleep 10
    
    # Check service status
    print_info "Checking service status..."
    docker-compose ps
    
    echo ""
    print_header "Bootstrap Complete!"
    echo ""
    print_success "Titan Server is starting up!"
    echo ""
    print_info "Services:"
    echo "  • Minecraft Server: localhost:25565"
    echo "  • Grafana Dashboard: http://localhost:3000 (admin/admin)"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • PostgreSQL: localhost:5432 (titan/changeme_in_production)"
    echo "  • Redis: localhost:6379"
    echo ""
    print_info "Useful commands:"
    echo "  • View logs: docker-compose logs -f"
    echo "  • Stop services: docker-compose down"
    echo "  • Rebuild: docker-compose up -d --build"
    echo "  • Status: docker-compose ps"
    echo ""
    print_warning "Note: Services may take 1-2 minutes to fully start"
    print_info "Watch logs with: docker-compose logs -f titan-proxy"
    echo ""
}

# Run main function
main "$@"
