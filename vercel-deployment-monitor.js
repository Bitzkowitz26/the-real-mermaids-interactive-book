#!/usr/bin/env node

/**
 * 🚀 VERCEL DEPLOYMENT MONITOR
 * Prevents deployment issues by monitoring status and alerting on problems
 * Usage: node vercel-deployment-monitor.js <project-name> [options]
 */

const https = require('https');
const fs = require('fs');

class VercelDeploymentMonitor {
    constructor(projectName, options = {}) {
        this.projectName = projectName;
        this.options = {
            checkInterval: options.checkInterval || 300000, // 5 minutes
            alertOnRollback: options.alertOnRollback !== false,
            alertOnFailure: options.alertOnFailure !== false,
            logFile: options.logFile || 'deployment-monitor.log',
            ...options
        };
        this.lastKnownStatus = null;
        this.lastKnownCommit = null;
    }

    log(message, level = 'INFO') {
        const timestamp = new Date().toISOString();
        const logEntry = `[${timestamp}] [${level}] ${message}\n`;
        
        console.log(logEntry.trim());
        
        if (this.options.logFile) {
            fs.appendFileSync(this.options.logFile, logEntry);
        }
    }

    async makeRequest(url, options = {}) {
        return new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve(data);
                    }
                });
            });
            
            req.on('error', reject);
            req.end();
        });
    }

    async checkDeploymentStatus() {
        try {
            this.log(`Checking deployment status for ${this.projectName}...`);
            
            // Note: This is a simplified version. In production, you'd use Vercel API
            // For now, we'll simulate the check with a site content verification
            const siteCheck = await this.checkSiteContent();
            
            return {
                status: siteCheck.accessible ? 'ready' : 'error',
                commit: siteCheck.commit || 'unknown',
                url: siteCheck.url,
                timestamp: new Date().toISOString(),
                content: siteCheck.content
            };
            
        } catch (error) {
            this.log(`Error checking deployment: ${error.message}`, 'ERROR');
            return {
                status: 'error',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async checkSiteContent() {
        const domains = [
            'kidsbook.dev',
            'www.kidsbook.dev',
            'the-real-mermaids-interactive-book-git-main-bitzkowitz26s-projects.vercel.app'
        ];

        for (const domain of domains) {
            try {
                const url = `https://${domain}/`;
                const response = await this.makeRequest(url);
                
                // Extract key content indicators
                const titleMatch = response.match(/<title>(.*?)<\/title>/);
                const h1Match = response.match(/<h1[^>]*>(.*?)<\/h1>/);
                
                const title = titleMatch ? titleMatch[1].replace(/<[^>]*>/g, '').trim() : '';
                const heading = h1Match ? h1Match[1].replace(/<[^>]*>/g, '').trim() : '';
                
                // Check for interactive book content
                const hasBookContent = response.includes('Real Mermaids') || 
                                     response.includes('Interactive Book') || 
                                     response.includes('Raquel');
                
                // Check for old design
                const hasOldDesign = response.includes('Create Amazing Stories');
                
                return {
                    accessible: true,
                    url: url,
                    title: title,
                    heading: heading,
                    hasBookContent: hasBookContent,
                    hasOldDesign: hasOldDesign,
                    content: {
                        title: title,
                        heading: heading,
                        hasBookContent: hasBookContent,
                        isModernDesign: !hasOldDesign && hasBookContent
                    }
                };
                
            } catch (error) {
                this.log(`Failed to check ${domain}: ${error.message}`, 'WARN');
                continue;
            }
        }
        
        return { accessible: false, error: 'All domains failed' };
    }

    async detectChanges(currentStatus) {
        const changes = [];
        
        if (this.lastKnownStatus && this.lastKnownStatus.status !== currentStatus.status) {
            changes.push({
                type: 'status_change',
                from: this.lastKnownStatus.status,
                to: currentStatus.status,
                severity: currentStatus.status === 'error' ? 'high' : 'medium'
            });
        }
        
        if (currentStatus.content && this.lastKnownStatus?.content) {
            if (currentStatus.content.heading !== this.lastKnownStatus.content.heading) {
                changes.push({
                    type: 'content_change',
                    field: 'heading',
                    from: this.lastKnownStatus.content.heading,
                    to: currentStatus.content.heading,
                    severity: 'medium'
                });
            }
            
            if (currentStatus.content.isModernDesign !== this.lastKnownStatus.content.isModernDesign) {
                changes.push({
                    type: 'design_change',
                    from: this.lastKnownStatus.content.isModernDesign ? 'modern' : 'old',
                    to: currentStatus.content.isModernDesign ? 'modern' : 'old',
                    severity: 'high'
                });
            }
        }
        
        return changes;
    }

    async sendAlert(changes, currentStatus) {
        for (const change of changes) {
            let message = '';
            
            switch (change.type) {
                case 'status_change':
                    message = `🚨 DEPLOYMENT STATUS CHANGED: ${change.from} → ${change.to}`;
                    break;
                case 'content_change':
                    message = `📝 CONTENT CHANGED (${change.field}): "${change.from}" → "${change.to}"`;
                    break;
                case 'design_change':
                    message = `🎨 DESIGN CHANGED: ${change.from} → ${change.to}`;
                    if (change.to === 'old') {
                        message += ' ⚠️ OLD DESIGN DETECTED!';
                    }
                    break;
            }
            
            this.log(message, change.severity === 'high' ? 'ALERT' : 'WARN');
            
            // In production, send to Slack, email, etc.
            if (change.severity === 'high') {
                this.log('🚨 HIGH SEVERITY ALERT - Manual intervention may be required', 'ALERT');
            }
        }
    }

    async runHealthCheck() {
        this.log('🔍 Running deployment health check...');
        
        const status = await this.checkDeploymentStatus();
        const changes = await this.detectChanges(status);
        
        if (changes.length > 0) {
            await this.sendAlert(changes, status);
        } else {
            this.log('✅ No changes detected - deployment healthy');
        }
        
        // Update tracking
        this.lastKnownStatus = status;
        
        // Log current status
        if (status.content) {
            this.log(`Current status: ${status.status} | Title: "${status.content.title}" | Book Content: ${status.content.hasBookContent ? 'Yes' : 'No'} | Design: ${status.content.isModernDesign ? 'Modern' : 'Old'}`);
        }
        
        return status;
    }

    start() {
        this.log(`🚀 Starting deployment monitor for ${this.projectName}`);
        this.log(`Check interval: ${this.options.checkInterval / 1000}s`);
        
        // Initial check
        this.runHealthCheck();
        
        // Set up periodic checks
        setInterval(() => {
            this.runHealthCheck();
        }, this.options.checkInterval);
        
        this.log('✅ Deployment monitor started');
    }

    async runOnce() {
        this.log(`🔍 Running one-time health check for ${this.projectName}`);
        const status = await this.runHealthCheck();
        
        // Exit with appropriate code
        if (status.status === 'ready' && status.content?.isModernDesign && status.content?.hasBookContent) {
            this.log('✅ Deployment is healthy - Interactive book content detected');
            process.exit(0);
        } else {
            this.log('❌ Deployment issues detected');
            if (!status.content?.hasBookContent) {
                this.log('   - Missing interactive book content');
            }
            if (!status.content?.isModernDesign) {
                this.log('   - Old design detected or content issues');
            }
            process.exit(1);
        }
    }
}

// CLI Usage
if (require.main === module) {
    const args = process.argv.slice(2);
    const projectName = args[0];
    
    if (!projectName) {
        console.log('Usage: node vercel-deployment-monitor.js <project-name> [--once]');
        console.log('Example: node vercel-deployment-monitor.js the-real-mermaids-interactive-book');
        console.log('Default: node vercel-deployment-monitor.js kidsbook-dev --once');
        process.exit(1);
    }
    
    const options = {
        checkInterval: 300000, // 5 minutes
        logFile: `deployment-monitor-${projectName}.log`
    };
    
    const monitor = new VercelDeploymentMonitor(projectName, options);
    
    if (args.includes('--once')) {
        monitor.runOnce();
    } else {
        monitor.start();
        
        // Graceful shutdown
        process.on('SIGINT', () => {
            monitor.log('🛑 Deployment monitor stopped');
            process.exit(0);
        });
    }
}

module.exports = VercelDeploymentMonitor;