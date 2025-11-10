#!/bin/bash
# Quick push script for Git Bash

echo "Pushing to GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ SUCCESS!"
    echo ""
    echo "Creating release tag..."
    git tag -a v1.0.0-alpha -m "Initial alpha release"
    git push origin v1.0.0-alpha
    echo ""
    echo "View at: https://github.com/galion-studio/project-mc.galion.studio"
else
    echo ""
    echo "✗ FAILED"
    echo "Create repo first: https://github.com/organizations/galion-studio/repositories/new"
    echo "Name: project-mc.galion.studio"
fi

