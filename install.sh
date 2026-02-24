#!/bin/bash
###############################################################################
# Zadara Storage MCP Server - Installation Script
# Version: 1.3.0
# Date: 2026-02-24
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║        Zadara Storage MCP Server - Installation           ║${NC}"
echo -e "${BLUE}║                    Version 1.3.0                           ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print step
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Function to print error
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check Python installation
print_step "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check pip installation
print_step "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi
print_success "pip3 found"

# Install dependencies
print_step "Installing Python dependencies..."
cd "$SCRIPT_DIR"
pip3 install -r requirements.txt --quiet
print_success "Dependencies installed"

# Configuration setup
echo ""
print_step "Configuration Setup"
echo ""

if [ -f .env ]; then
    print_warning ".env file already exists. Skipping configuration setup."
    print_warning "To reconfigure, delete .env and run this script again."
else
    echo "This server requires API credentials for Zadara Storage."
    echo ""
    
    read -p "Do you want to configure credentials now? (y/n): " configure_now
    
    if [ "$configure_now" = "y" ] || [ "$configure_now" = "Y" ]; then
        echo ""
        echo -e "${YELLOW}VPSA Storage Array Configuration${NC}"
        echo "If you don't have VPSA credentials, press Enter to skip."
        echo ""
        
        read -p "VPSA URL (e.g., https://your-vpsa.zadarazios.com): " vpsa_url
        read -p "VPSA API Key: " vpsa_key
        
        echo ""
        echo -e "${YELLOW}Object Storage Configuration${NC}"
        echo "If you don't have Object Storage credentials, press Enter to skip."
        echo ""
        
        read -p "Object Storage URL (e.g., https://your-storage.zadarazios.com): " obj_url
        read -p "Object Storage Access Key: " obj_access
        read -p "Object Storage Secret Key: " obj_secret
        
        # Create .env file
        cat > .env << EOF
# Zadara Storage MCP Server Configuration
# Version 1.3.0

# VPSA Storage Array Configuration
ZADARA_VPSA_URL=$vpsa_url
ZADARA_VPSA_API_KEY=$vpsa_key

# Object Storage Configuration
ZADARA_OBJECT_STORAGE_URL=$obj_url
ZADARA_OBJECT_ACCESS_KEY=$obj_access
ZADARA_OBJECT_SECRET_KEY=$obj_secret
EOF
        
        print_success "Configuration saved to .env"
    else
        print_warning "Skipping configuration. You can configure later by editing .env file."
        print_warning "See .env.example for reference."
    fi
fi

# Test installation
echo ""
print_step "Testing installation..."
if python3 -c "import httpx; from mcp.server import Server" 2>/dev/null; then
    print_success "All dependencies are correctly installed"
else
    print_error "Dependency check failed. Please check the installation."
    exit 1
fi

# Check if server.py is executable
if [ ! -x "$SCRIPT_DIR/server.py" ]; then
    chmod +x "$SCRIPT_DIR/server.py"
    print_success "Made server.py executable"
fi

# Installation summary
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║              Installation Complete! 🎉                     ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Next steps
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Configure credentials (if not done):"
echo "   Edit the .env file with your Zadara Storage credentials"
echo ""
echo "2. Test the server:"
echo "   python3 server.py"
echo ""
echo "3. Integrate with Claude Desktop:"
echo "   See QUICKSTART.md for detailed instructions"
echo ""
echo "4. Try the new bucket size calculation feature:"
echo "   Ask Claude: 'Show me the size of all my buckets'"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   README.md          - Complete documentation"
echo "   QUICKSTART.md      - Quick start guide"
echo "   EXAMPLES.md        - Usage examples"
echo "   CHANGELOG.md       - Version history"
echo ""
echo -e "${BLUE}New in v1.3.0:${NC}"
echo "   • Bucket size calculation tool"
echo "   • Automatic pagination support"
echo "   • Human-readable size formatting"
echo "   • Per-bucket and summary statistics"
echo ""
echo "For support and issues, see CONTRIBUTING.md"
echo ""
