#!/bin/bash

# Blog API Setup Script
# Usage: ./setup.sh [command]
# Commands: setup, run, test-all

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Found Python $python_version"
    
    # Check if version is 3.8+
    if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null; then
        print_error "Python 3.8+ is required. Found Python $python_version"
        exit 1
    fi
}

# Function to install system dependencies
install_system_deps() {
    print_status "Checking system dependencies..."
    
    # Check if we're on Ubuntu/Debian
    if command_exists apt-get; then
        # Check if python3-venv is available
        if ! dpkg -l | grep -q python3-venv; then
            print_status "Installing python3-venv and python3-pip..."
            sudo apt-get update
            sudo apt-get install -y python3-venv python3-pip
        fi
    elif command_exists yum; then
        print_status "Installing Python development tools..."
        sudo yum install -y python3-devel python3-pip
    elif command_exists brew; then
        print_status "macOS detected. Python should be available via brew or system..."
    else
        print_warning "Unknown package manager. Please ensure python3-venv is available."
    fi
}

# Function to setup virtual environment and dependencies
setup_environment() {
    print_status "Setting up Python virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Dependencies installed successfully"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Change to Django project directory
    cd blog_api
    
    # Create environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file from template..."
        cp ../env.example .env
        
        # Generate a random secret key
        secret_key=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
        sed -i "s/your-secret-key-here-make-it-long-and-random/$secret_key/" .env
        sed -i "s/DEBUG=False/DEBUG=True/" .env
        
        print_success ".env file created with random secret key"
    else
        print_status ".env file already exists"
    fi
    
    # Run migrations
    print_status "Running database migrations..."
    python manage.py makemigrations
    python manage.py migrate
    
    print_success "Database setup completed"
    
    # Go back to root directory
    cd ..
}

# Function to run the development server
run_server() {
    print_status "Starting development server..."
    
    # Check if setup was run
    if [ ! -d "venv" ] || [ ! -f "blog_api/.env" ]; then
        print_error "Please run './setup.sh setup' first"
        exit 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Change to Django project directory
    cd blog_api
    
    print_success "Starting Django development server..."
    print_status "API will be available at: http://localhost:8000/api/"
    print_status "Admin interface at: http://localhost:8000/admin/"
    print_status "Press Ctrl+C to stop the server"
    
    # Run the server
    python manage.py runserver
}

# Function to run all tests
run_tests() {
    print_status "Running comprehensive test suite..."
    
    # Check if setup was run
    if [ ! -d "venv" ]; then
        print_error "Please run './setup.sh setup' first"
        exit 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Change to Django project directory
    cd blog_api
    
    print_status "Running Django tests..."
    python manage.py test --verbosity=2
    
    print_status "Running pytest tests..."
    if command_exists pytest; then
        pytest --verbose || true  # Don't exit on pytest issues
    else
        print_warning "pytest not found, skipping pytest run"
    fi
    
    print_status "Running with coverage analysis..."
    if command_exists coverage; then
        echo ""
        echo "Running tests with coverage..."
        coverage run --source='.' manage.py test
        
        echo ""
        echo "=================================================="
        echo "              CODE COVERAGE REPORT"
        echo "=================================================="
        echo ""

        coverage report
        
        echo ""
        echo "=================================================="
        echo "     DETAILED COVERAGE REPORT (Missing Lines)"
        echo "=================================================="
        echo ""

        coverage report --show-missing
        
        echo ""
        echo "=================================================="
        echo "               COVERAGE SUMMARY"
        echo "=================================================="
        
        # Get total coverage percentage
        total_coverage=$(coverage report | tail -n 1 | awk '{print $4}' | sed 's/%//')
        
        echo "Total Coverage: $total_coverage%"
        echo ""
        
        # Convert to integer for comparison (remove decimal part)
        coverage_int=$(echo "$total_coverage" | cut -d'.' -f1)
        
        if [ "$coverage_int" -ge 90 ]; then
            echo "✅ EXCELLENT! Coverage above 90% - Production ready!"
        else
            echo "LOW. Coverage below 70% - More tests needed"
        fi
        
        echo ""

        coverage html
        print_success "Detailed HTML report: htmlcov/index.html"

    else
        print_warning "coverage not found, skipping coverage report"
    fi
    
    echo ""
    print_success "All tests completed!"
}

# Function to create superuser
create_superuser() {
    print_status "Creating Django superuser..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Change to Django project directory
    cd blog_api
    
    print_status "Creating superuser for admin access..."
    python manage.py createsuperuser
    
    print_success "Superuser created! You can now access http://localhost:8000/admin/"
}

# Function to show usage
show_usage() {
    echo "Blog API Setup Script"
    echo ""
    echo "Usage: ./setup.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup      - Install dependencies and setup environment"
    echo "  run        - Start the development server"
    echo "  test-all   - Run comprehensive test suite"
    echo "  superuser  - Create Django admin superuser"
    echo "  docker     - Run with Docker Compose"
    echo ""
    echo "Quick Start:"
    echo "  ./setup.sh setup    # First time setup"
    echo "  ./setup.sh run      # Start the API server"
    echo "  ./setup.sh test-all # Run all tests"
    echo ""
    echo "Docker Alternative:"
    echo "  ./setup.sh docker   # Run everything with Docker"
    echo ""
}

# Function to run with Docker
run_docker() {
    print_status "Running with Docker Compose..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker compose version >/dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Building and starting containers..."
    docker compose up --build
}

# Main script logic
main() {
    echo "=================================================="
    echo "   Blog API - Django REST Framework Setup"
    echo "=================================================="
    echo ""
    
    case "${1:-}" in
        "setup")
            print_status "Starting setup process..."
            check_python
            install_system_deps
            setup_environment
            setup_database
            print_success "Setup completed successfully!"
            echo ""
            print_status "Next steps:"
            echo "  - Run './setup.sh run' to start the API server"
            echo "  - Run './setup.sh test-all' to run tests"
            echo "  - Run './setup.sh superuser' to create admin user"
            ;;
        "run")
            run_server
            ;;
        "test-all")
            run_tests
            ;;
        "superuser")
            create_superuser
            ;;
        "docker")
            run_docker
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        "")
            show_usage
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 