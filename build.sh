#!/bin/bash
set -e

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Listing contents:"
ls -la

echo "Navigating to client directory..."
cd client

echo "Installing dependencies..."
npm install

echo "Building the application..."
npm run build

echo "Build completed successfully!"
echo "Build output directory: $(pwd)/dist"
ls -la dist/ 