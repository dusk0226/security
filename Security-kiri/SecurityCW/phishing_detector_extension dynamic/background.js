const FEED_URL = "https://gist.githubusercontent.com/Goonshan/a5913c6bf9be3c59e809197383410f39/raw/fae1b188eb0ed012b74c86548d80d1edafb10bb7/feed.txt";

fetch(FEED_URL)
  .then(response => response.text())
  .then(text => {
    const urls = text.trim().split("\n");
    const domains = urls.map(url => {
      try {
        const parsedUrl = new URL(url);
        return parsedUrl.hostname;
      } catch (e) {
        console.error("Invalid URL:", url);
        return null;
      }
    }).filter(domain => domain);

    const rules = domains.slice(0, 1000).map((domain, index) => ({
      id: index + 1,
      priority: 1,
      action: { type: "block" },
      condition: {
        urlFilter: `||${domain}^`,
        resourceTypes: ["main_frame"]
      }
    }));

    chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: rules.map(rule => rule.id),
      addRules: rules
    }).then(() => {
      console.log("✅ OpenPhish domains blocked:", domains);
    }).catch(err => console.error("Error updating rules:", err));
  }).catch(err => console.error("Failed to fetch OpenPhish feed:", err));
