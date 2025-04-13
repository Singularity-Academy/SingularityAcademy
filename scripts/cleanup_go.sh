#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Go Project Cleanup Script${NC}"
echo "=========================="
echo

# List of directories to clean
CLEAN_DIRS=(
    "backend/go/pkg"
    "backend/go/bin"
    "backend/pkg/mod"
    "backend/pkg/sumdb"
    "backend/.go"
    "backend/go-build"
)

# Function to format size
format_size() {
    local size=$1
    if [ $size -ge 1073741824 ]; then
        echo "$(( size / 1073741824 )) GB"
    elif [ $size -ge 1048576 ]; then
        echo "$(( size / 1048576 )) MB"
    elif [ $size -ge 1024 ]; then
        echo "$(( size / 1024 )) KB"
    else
        echo "$size bytes"
    fi
}

# Calculate total size before cleanup
total_size=0
for dir in "${CLEAN_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        size=$(du -sb "$dir" 2>/dev/null | cut -f1)
        total_size=$((total_size + size))
        echo -e "${YELLOW}Found${NC} $dir ($(format_size $size))"
    fi
done

if [ $total_size -eq 0 ]; then
    echo -e "\n${GREEN}No Go temporary files found to clean up.${NC}"
    exit 0
fi

echo -e "\nTotal space used: ${YELLOW}$(format_size $total_size)${NC}"

# Ask for confirmation
read -p $'\nDo you want to remove these directories? (y/N) ' -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Cleaning up Go temporary files...${NC}"
    
    for dir in "${CLEAN_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            if rm -rf "$dir"; then
                echo -e "✓ Removed: ${GREEN}$dir${NC}"
            else
                echo -e "✗ Failed to remove: ${RED}$dir${NC}"
            fi
        fi
    done
    
    echo -e "\n${GREEN}Cleanup completed!${NC}"
    echo "You can restore these files by:"
    echo "1. Running './scripts/setup_go.sh' to reinstall Go"
    echo "2. Running 'go mod download' to restore dependencies"
    echo "3. Running 'go build' to rebuild any necessary binaries"
else
    echo -e "\n${YELLOW}Operation cancelled by user.${NC}"
fi 