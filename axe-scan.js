const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const AxeBuilder = require('@axe-core/webdriverjs');
const fs = require('fs');

// Get URLs from command line args
const urls = process.argv.slice(2);
console.log(`\nStarting Axe scan on ${urls.length} pages...\n`);

(async function scan() {
  const options = new chrome.Options();
  options.addArguments('--headless=new'); 
  options.addArguments('--no-sandbox');
  options.addArguments('--disable-dev-shm-usage'); 
  options.addArguments('--disable-gpu');
  // see if these help with the production/shifts page crashing
  options.addArguments('--window-size=1920,1080');
  options.addArguments('--disable-extensions');
  options.addArguments('--disable-infobars');
  options.addArguments('--disable-software-rasterizer');
  
  // Initialize Driver
  const driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

  const fullReport = [];
  let hasErrors = false;

  try {
    // Set a very generous timeout for page loads (3 minutes)
    await driver.manage().setTimeouts({ pageLoad: 180000, script: 180000 });

    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      console.log(`[${i + 1}/${urls.length}] Testing ${url} ...`);

      try {
        await driver.get(url);

        const results = await new AxeBuilder(driver)
          .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
          .analyze();

        if (results.violations.length > 0) {
          console.log(`  FAILED: ${results.violations.length} violations found.`);
          results.violations.forEach((violation) => {
            console.log(`    [${violation.impact.toUpperCase()}] ${violation.id}: ${violation.help}`);
            console.log(`    Help URL: ${violation.helpUrl}`);
            
            violation.nodes.forEach((node) => {
               console.log(`      - Selector: ${node.target.join(' ')}`);
            });
            console.log(''); // Empty line for readability
          });

          fullReport.push({
            url: url,
            violations: results.violations
          });
          hasErrors = true;
        } else {
          console.log(`  PASSED`);
        }

      } catch (e) {
        console.error(`  CRASHED: Could not scan ${url}. Skipping.`);
        console.error(`  Reason: ${e.message}`);
        fullReport.push({
          url: url,
          error: "Browser crashed or timed out on this page",
          details: e.message
        });
        hasErrors = true;
      }
    }

    // Save JSON report
    fs.writeFileSync('axe-report.json', JSON.stringify(fullReport, null, 2));
    console.log('\nReport saved to axe-report.json');

  } finally {
    await driver.quit();
  }

  if (hasErrors) {
    process.exit(1);
  }
})();