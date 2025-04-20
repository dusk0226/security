// Load the JSON file and block the domains
fetch(chrome.runtime.getURL("phishing_domains.json"))
  .then(response => response.json())
  .then(domains => {
    const rules = domains.map((domain, index) => ({
      id: index + 1,
      priority: 1,
      action: { type: "block" },
      condition: {
        urlFilter: `||${domain}^`,
        resourceTypes: ["main_frame"]
      }
    }));

    // Clear old rules and add new ones
    chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: rules.map(rule => rule.id),
      addRules: rules
    }).then(() => {
      console.log("Phishing domains blocked:", domains);
    }).catch(err => console.error("Error updating rules:", err));
  }).catch(err => console.error("Failed to load domain list:", err));
