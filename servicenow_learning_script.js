#!/usr/bin/env node
/**
 * ServiceNow Knowledge Learning Script
 * Uses Tavily Search to gather ServiceNow documentation updates
 * Runs twice a week
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG = {
    outputDir: '/root/.openclaw/workspace/solution/servicenow_knowledge',
    topics: [
        { name: 'event-management', query: 'ServiceNow Yokohama Event Management new features 2026' },
        { name: 'ai-search', query: 'ServiceNow AI Search configuration best practices 2026' },
        { name: 'itsm', query: 'ServiceNow ITSM latest updates features 2026' },
        { name: 'itom', query: 'ServiceNow ITOM monitoring AIOps updates 2026' },
        { name: 'hr-service-delivery', query: 'ServiceNow HR Service Delivery employee center 2026' },
        { name: 'security-operations', query: 'ServiceNow SecOps security operations updates 2026' },
        { name: 'app-engine', query: 'ServiceNow App Engine low code development 2026' },
        { name: 'integration-hub', query: 'ServiceNow Integration Hub connectors API 2026' },
        { name: 'agentic-ai', query: 'ServiceNow Agentic AI autonomous agents 2026' },
        { name: 'now-assist', query: 'ServiceNow Now Assist generative AI features 2026' }
    ]
};

function searchWithTavily(query) {
    try {
        const result = execSync(
            `python3 /root/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py --query "${query}" --max-results 5 --format md`,
            { encoding: 'utf-8', timeout: 60000 }
        );
        return { success: true, content: result };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function main() {
    console.log(`[${new Date().toISOString()}] Starting ServiceNow Knowledge Learning...`);
    
    // Ensure output directory exists
    if (!fs.existsSync(CONFIG.outputDir)) {
        fs.mkdirSync(CONFIG.outputDir, { recursive: true });
    }
    
    const results = [];
    
    for (const topic of CONFIG.topics) {
        console.log(`Searching: ${topic.name}`);
        
        const result = searchWithTavily(topic.query);
        results.push({
            topic: topic.name,
            query: topic.query,
            ...result
        });
        
        if (result.success) {
            const filename = `${topic.name}_${Date.now()}.md`;
            fs.writeFileSync(
                path.join(CONFIG.outputDir, filename),
                result.content
            );
            console.log(`  ✓ Saved: ${filename}`);
        } else {
            console.log(`  ✗ Failed: ${result.error}`);
        }
        
        // Wait between requests to avoid rate limiting
        await new Promise(r => setTimeout(r, 3000));
    }
    
    // Generate summary report
    const report = {
        timestamp: new Date().toISOString(),
        totalTopics: CONFIG.topics.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        results
    };
    
    const reportFile = `report_${Date.now()}.json`;
    fs.writeFileSync(
        path.join(CONFIG.outputDir, reportFile),
        JSON.stringify(report, null, 2)
    );
    
    // Create consolidated knowledge file
    const consolidatedKnowledge = results
        .filter(r => r.success)
        .map(r => `## ${r.topic.toUpperCase()}\n\nQuery: ${r.query}\n\n${r.content}`)
        .join('\n\n---\n\n');
    
    fs.writeFileSync(
        path.join(CONFIG.outputDir, `consolidated_knowledge_${Date.now()}.md`),
        `# ServiceNow Knowledge Update - ${new Date().toISOString().split('T')[0]}\n\n${consolidatedKnowledge}`
    );
    
    console.log(`[${new Date().toISOString()}] Learning complete!`);
    console.log(`  Success: ${report.successful}/${report.totalTopics}`);
    console.log(`  Report: ${reportFile}`);
}

main().catch(console.error);
