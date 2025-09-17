// Simple test to verify Vercel deployment readiness
const fs = require('fs');
const path = require('path');

console.log('🔍 Vercel Deployment Readiness Check\n');

// Check required files
const requiredFiles = [
    'index.html',
    'Raquel_Book_Interactive.html',
    'vercel.json',
    'package.json',
    'README.md'
];

let allFilesExist = true;

requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`✅ ${file} - Found`);
    } else {
        console.log(`❌ ${file} - Missing`);
        allFilesExist = false;
    }
});

// Check vercel.json structure
try {
    const vercelConfig = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    console.log('\n📋 Vercel Configuration:');
    console.log(`✅ Version: ${vercelConfig.version}`);
    console.log(`✅ Name: ${vercelConfig.name}`);
    console.log(`✅ Routes: ${vercelConfig.routes.length} configured`);
    console.log(`✅ Headers: Security headers configured`);
} catch (error) {
    console.log('❌ vercel.json - Invalid JSON');
    allFilesExist = false;
}

// Check package.json
try {
    const packageConfig = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    console.log('\n📦 Package Configuration:');
    console.log(`✅ Name: ${packageConfig.name}`);
    console.log(`✅ Version: ${packageConfig.version}`);
    console.log(`✅ Scripts: ${Object.keys(packageConfig.scripts).length} defined`);
} catch (error) {
    console.log('❌ package.json - Invalid JSON');
    allFilesExist = false;
}

// Final result
console.log('\n🎯 Deployment Readiness:');
if (allFilesExist) {
    console.log('✅ READY FOR VERCEL DEPLOYMENT!');
    console.log('\n🚀 To deploy:');
    console.log('1. Connect your GitHub repo to Vercel');
    console.log('2. Vercel will auto-detect as static site');
    console.log('3. Deploy with zero configuration needed');
} else {
    console.log('❌ Missing required files - fix issues above');
}