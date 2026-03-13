#!/usr/bin/env node
/**
 * ServiceNow Documentation Learning Script
 * Runs twice a week to scrape and learn new content
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CONFIG = {
    baseUrl: 'https://www.servicenow.com/docs/',
    outputDir: '/root/.openclaw/workspace/solution/servicenow_knowledge',
    topics: [
        'event-management',
        'ai-search',
        'itsm',
        'itom',
        'hr-service-delivery',
        'security-operations',
        'app-engine',
        'integration-hub'
    ]
};

async function scrapeTopic(page, topic) {
    const url = `${CONFIG.baseUrl}r/yokohama/it-operations-management/${topic}/`;
    console.log(`Scraping: ${url}`);
    
    try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(5000);
        
        const content = await page.evaluate(() => {
            const title = document.querySelector('h1')?.textContent?.trim() || '';
            const headings = Array.from(document.querySelectorAll('h2, h3'))
                .map(h => h.textContent.trim())
                .filter(t => t.length > 0);
            const paragraphs = Array.from(document.querySelectorAll('p'))
                .map(p => p.textContent.trim())
                .filter(t => t.length > 100);
            
            return { title, headings, paragraphs: paragraphs.slice(0, 20) };
        });
        
        return { topic, url, success: true, content };
    } catch (error) {
        return { topic, url, success: false, error: error.message };
    }
}

async function main() {
    console.log(`[${new Date().toISOString()}] Starting ServiceNow Learning...`);
    
    // Ensure output directory exists
    if (!fs.existsSync(CONFIG.outputDir)) {
        fs.mkdirSync(CONFIG.outputDir, { recursive: true });
    }
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });
    const page = await context.newPage();
    
    const results = [];
    
    for (const topic of CONFIG.topics) {
        const result = await scrapeTopic(page, topic);
        results.push(result);
        
        if (result.success) {
            const filename = `${topic}_${Date.now()}.json`;
            fs.writeFileSync(
                path.join(CONFIG.outputDir, filename),
                JSON.stringify(result, null, 2)
            );
            console.log(`  ✓ Saved: ${filename}`);
        } else {
            console.log(`  ✗ Failed: ${result.error}`);
        }
        
        // Wait between requests
        await new Promise(r => setTimeout(r, 3000));
    }
    
    await browser.close();
    
    // Generate summary report
    const report = {
        timestamp: new Date().toISOString(),
        totalTopics: CONFIG.topics.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        results
    };
    
    fs.writeFileSync(
        path.join(CONFIG.outputDir, `report_${Date.now()}.json`),
        JSON.stringify(report, null, 2)
    );
    
    console.log(`[${new Date().toISOString()}] Learning complete!`);
    console.log(`  Success: ${report.successful}/${report.totalTopics}`);
}

main().catch(console.error);
