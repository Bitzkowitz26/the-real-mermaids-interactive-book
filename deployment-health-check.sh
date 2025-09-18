#!/bin/bash

# 🚀 DEPLOYMENT HEALTH CHECK TOOL - KIDSBOOK.DEV
# Prevents 3-day debugging nightmares by checking the obvious first
# Usage: ./deployment-health-check.sh [domain] [vercel-project-name]

set -e

DOMAIN=${1:-"kidsbook.dev"}
VERCEL_PROJECT=${2:-"the-real-mermaids-interactive-book"}
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🔍 DEPLOYMENT HEALTH CHECK - $TIMESTAMP"
echo "=================================================="

echo "🌐 Domain: $DOMAIN"
echo "📦 Vercel Project: $VERCEL_PROJECT"
echo ""

# 1. Site Accessibility Check
echo "1️⃣ SITE ACCESSIBILITY CHECK"
echo "----------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Site accessible (HTTP $HTTP_CODE)"
else
    echo "❌ Site not accessible (HTTP $HTTP_CODE)"
    echo "🔍 Check: Authentication protection, DNS, SSL"
fi
echo ""

# 2. Content Verification
echo "2️⃣ CONTENT VERIFICATION"
echo "------------------------"
TITLE=$(curl -s "https://$DOMAIN/" | grep -E "<title>.*</title>" | sed 's/<[^>]*>//g' | xargs || echo "No title found")
H1_CONTENT=$(curl -s "https://$DOMAIN/" | grep -E "<h1.*>.*</h1>" | sed 's/<[^>]*>//g' | xargs || echo "No h1 found")

echo "📄 Page Title: $TITLE"
echo "📝 Main Heading: $H1_CONTENT"

# Check for interactive book content
BOOK_CONTENT_CHECK=$(curl -s "https://$DOMAIN/" | grep -E "(Real Mermaids|Interactive Book|Raquel)" || echo "")
if [ -n "$BOOK_CONTENT_CHECK" ]; then
    echo "✅ Interactive book content detected"
else
    echo "⚠️  Expected book content not found"
fi

# Check for old design indicators (if any)
OLD_DESIGN_CHECK=$(curl -s "https://$DOMAIN/" | grep -E "Create Amazing Stories" || echo "")
if [ -n "$OLD_DESIGN_CHECK" ]; then
    echo "⚠️  OLD DESIGN DETECTED: Found 'Create Amazing Stories' text"
else
    echo "✅ No old design remnants detected"
fi
echo ""

# 3. Repository Status Check
echo "3️⃣ REPOSITORY STATUS CHECK"
echo "---------------------------"
if [ -d ".git" ]; then
    CURRENT_BRANCH=$(git branch --show-current)
    LATEST_COMMIT=$(git rev-parse --short HEAD)
    COMMIT_MESSAGE=$(git log -1 --pretty=format:"%s")
    
    echo "🌿 Current Branch: $CURRENT_BRANCH"
    echo "📝 Latest Commit: $LATEST_COMMIT"
    echo "💬 Commit Message: $COMMIT_MESSAGE"
    
    # Check if working directory is clean
    if git diff-index --quiet HEAD --; then
        echo "✅ Working directory clean"
    else
        echo "⚠️  Uncommitted changes detected"
    fi
else
    echo "⚠️  Not in a git repository"
fi
echo ""

# 4. Vercel Integration Check
echo "4️⃣ VERCEL INTEGRATION CHECK"
echo "----------------------------"
echo "🔗 Vercel Dashboard: https://vercel.com/dashboard"
echo "📊 Project URL: https://vercel.com/bitzkowitz26s-projects/$VERCEL_PROJECT"
echo "🚀 Deployments: https://vercel.com/bitzkowitz26s-projects/$VERCEL_PROJECT/deployments"
echo ""
echo "⚠️  MANUAL CHECKS REQUIRED:"
echo "   1. Check deployment status (not 'Rolled Back')"
echo "   2. Verify latest commit is deployed"
echo "   3. Check authentication protection settings"
echo "   4. Review build logs for errors"
echo ""

# 5. Quick Fixes Checklist
echo "5️⃣ QUICK FIXES CHECKLIST"
echo "-------------------------"
echo "If issues found, try these in order:"
echo "□ 1. Check Vercel deployment status (rollback?)"
echo "□ 2. Disable Vercel authentication protection"
echo "□ 3. Trigger manual deployment from dashboard"
echo "□ 4. Check build configuration (vercel.json)"
echo "□ 5. Verify output directory settings"
echo "□ 6. Check domain DNS settings"
echo ""

# 6. Emergency Commands
echo "6️⃣ EMERGENCY COMMANDS"
echo "----------------------"
echo "Force new deployment:"
echo "  git commit --allow-empty -m 'Force deployment' && git push"
echo ""
echo "Trigger Vercel deploy hook (if available):"
echo "  curl -X POST 'https://api.vercel.com/v1/integrations/deploy/[HOOK_ID]'"
echo ""
echo "Check DNS propagation:"
echo "  dig $DOMAIN"
echo ""

echo "🎯 HEALTH CHECK COMPLETE - $TIMESTAMP"
echo "=================================================="

# Return appropriate exit code
if [ "$HTTP_CODE" = "200" ] && [ -n "$BOOK_CONTENT_CHECK" ] && [ -z "$OLD_DESIGN_CHECK" ]; then
    echo "✅ Overall Status: HEALTHY"
    exit 0
else
    echo "❌ Overall Status: ISSUES DETECTED"
    exit 1
fi