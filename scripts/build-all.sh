#!/bin/bash
# Galion Build Script
# Builds all components: API, plugins, server core, and Docker images

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

echo "========================================"
echo "  Galion Build System"
echo "  Building All Components"
echo "========================================"
echo ""

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v java &> /dev/null; then
    log_error "Java not found. Please install Java 17 or higher."
    exit 1
fi

if ! command -v mvn &> /dev/null; then
    log_warn "Maven not found. Attempting to use Maven wrapper..."
fi

if ! command -v docker &> /dev/null; then
    log_warn "Docker not found. Skipping Docker builds..."
    SKIP_DOCKER=true
fi

# Build API
log_info "Building Galion API..."
cd api
if [ -f "mvnw" ]; then
    ./mvnw clean package
else
    mvn clean package
fi
cd ..
log_info "API build complete"

# Build Server Core
log_info "Building hybrid server core..."
cd server-core
if [ -f "gradlew" ]; then
    ./gradlew clean buildServer
else
    gradle clean buildServer
fi
cd ..
log_info "Server core build complete"

# Build Custom Plugins (if any exist)
if [ -d "plugins" ] && [ "$(ls -A plugins)" ]; then
    log_info "Building custom plugins..."
    for plugin_dir in plugins/*/; do
        if [ -f "${plugin_dir}pom.xml" ]; then
            log_info "Building plugin: $(basename $plugin_dir)"
            cd "$plugin_dir"
            if [ -f "mvnw" ]; then
                ./mvnw clean package
            else
                mvn clean package
            fi
            cd ../..
        fi
    done
    log_info "Plugins build complete"
else
    log_info "No custom plugins to build"
fi

# Build Docker Images
if [ "$SKIP_DOCKER" != "true" ]; then
    log_info "Building Docker images..."
    
    # Build Velocity proxy image
    log_info "Building Velocity proxy image..."
    docker build -t galion/velocity-proxy:latest \
        -f infrastructure/docker/Dockerfile.velocity \
        infrastructure/docker/
    
    # Build server image
    log_info "Building hybrid server image..."
    docker build -t galion/hybrid-server:latest \
        -f infrastructure/docker/Dockerfile.server \
        .
    
    log_info "Docker images build complete"
else
    log_warn "Skipping Docker builds"
fi

# Summary
echo ""
echo "========================================"
echo "  Build Summary"
echo "========================================"
echo ""
log_info "✅ Galion API: api/target/galion-api-1.0.0.jar"
log_info "✅ Server Core: server-core/build/libs/galion-server-1.20.4.jar"

if [ "$SKIP_DOCKER" != "true" ]; then
    log_info "✅ Docker images built"
fi

echo ""
log_info "Build complete! 🚀"
log_info "Next steps:"
echo "  1. Test locally: docker-compose up -d"
echo "  2. Deploy to K8s: ./scripts/deploy.sh"

