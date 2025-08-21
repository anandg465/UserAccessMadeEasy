#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}========================================"
echo -e "  Oracle Fusion Resource Fetcher"
echo -e "========================================${NC}"
echo ""
echo -e "${YELLOW}Starting application...${NC}"
echo "This will open in your default web browser."
echo ""
echo "If the application doesn't start automatically,"
echo "please run: ./OracleFusionResourceFetcher"
echo ""

# Make executable if needed
if [ ! -x "./OracleFusionResourceFetcher" ]; then
    echo -e "${YELLOW}Making executable...${NC}"
    chmod +x ./OracleFusionResourceFetcher
fi

# Start the application
./OracleFusionResourceFetcher

echo ""
echo -e "${GREEN}Application started!${NC}"
echo "Check your web browser for the interface."
echo ""
