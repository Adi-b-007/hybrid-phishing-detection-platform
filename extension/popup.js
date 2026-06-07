let currentDomain = "";

// --------------------------------------------------
// GET CURRENT TAB URL
// --------------------------------------------------
chrome.tabs.query(
  {
    active: true,
    currentWindow: true
  },
  (tabs) => {

    if (tabs[0] && tabs[0].url) {

      currentDomain = tabs[0].url;

      document.getElementById(
        "current-url"
      ).innerText = currentDomain;

    }

  }
);

// --------------------------------------------------
// SCAN WEBSITE
// --------------------------------------------------
document
  .getElementById("scanBtn")
  .addEventListener(
    "click",
    async () => {

      try {

        // Prevent scanning browser pages
        if (
          currentDomain.startsWith("chrome://") ||
          currentDomain.startsWith("chrome-extension://")
        ) {

          alert(
            "This page cannot be scanned."
          );

          return;

        }

        const response =
          await fetch(
            "http://127.0.0.1:5000/predict",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json"
              },

              body: JSON.stringify({
                url: currentDomain
              })
            }
          );

        console.log(
          "Response Status:",
          response.status
        );

        const result =
          await response.json();

        console.log(
          "API Result:",
          result
        );

        if (result.error) {

          throw new Error(
            result.error
          );

        }

        // ----------------------------------
        // STATUS
        // ----------------------------------

        let statusHTML = "";

        if (
          result.prediction ===
          "Phishing"
        ) {

          statusHTML = `
            <div class="danger">
              ⚠ PHISHING DETECTED
            </div>

            <p>
              Confidence:
              ${result.confidence}%
            </p>
          `;

        } else {

          statusHTML = `
            <div class="safe">
              ✅ LEGITIMATE
            </div>

            <p>
              Confidence:
              ${result.confidence}%
            </p>
          `;

        }

        const resultBox =
          document.getElementById(
            "result"
          );

        if (resultBox) {

          resultBox.innerHTML =
            statusHTML;

        }

        // ----------------------------------
        // RISK BAR
        // ----------------------------------

        const riskFill =
          document.getElementById(
            "risk-fill"
          );

        if (riskFill) {

          riskFill.style.width =
            `${result.confidence}%`;

          riskFill.style.background =
            result.prediction ===
            "Phishing"
              ? "#ff4444"
              : "#00ff99";

        }

        const riskScore =
          document.getElementById(
            "risk-score"
          );

        if (riskScore) {

          riskScore.innerText =
            `${result.confidence}%`;

        }

        // ----------------------------------
        // DOMAIN INTELLIGENCE
        // ----------------------------------

        if (
          result.domain_info
        ) {

          const domainBox =
            document.getElementById(
              "domain-info"
            );

          if (domainBox) {

            domainBox.innerHTML = `
              <h3>
                Domain Intelligence
              </h3>

              <p>
                <strong>Domain:</strong>
                ${result.domain_info.domain}
              </p>

              <p>
                <strong>Protocol:</strong>
                ${result.domain_info.protocol}
              </p>

              <p>
                <strong>TLD:</strong>
                ${result.domain_info.tld}
              </p>

              <p>
                <strong>Length:</strong>
                ${result.domain_info.length}
              </p>

              <p>
                <strong>Hyphens:</strong>
                ${result.domain_info.hyphens}
              </p>

              <p>
                <strong>Risk:</strong>
                ${result.domain_info.risk_level}
              </p>
            `;

          }

        }

        // ----------------------------------
        // THREAT ANALYSIS
        // ----------------------------------

        let threatHTML =
          "<h3>Threat Analysis</h3>";

        if (
          result.reasons &&
          Array.isArray(
            result.reasons
          ) &&
          result.reasons.length > 0
        ) {

          result.reasons.forEach(
            (reason) => {

              threatHTML += `
                <p>
                  ⚠ ${reason}
                </p>
              `;

            }
          );

        } else {

          threatHTML += `
            <p class="safe">
              No suspicious indicators detected
            </p>
          `;

        }

        const threatBox =
          document.getElementById(
            "threat-analysis"
          );

        if (threatBox) {

          threatBox.innerHTML =
            threatHTML;

        }

      } catch (error) {

        console.error(error);

        const resultBox =
          document.getElementById(
            "result"
          );

        if (resultBox) {

          resultBox.innerHTML = `
            <div class="danger">
              ${error.message}
            </div>
          `;

        }

      }

    }
  );

// --------------------------------------------------
// BLOCK DOMAIN
// --------------------------------------------------
document
  .getElementById("blockBtn")
  .addEventListener(
    "click",
    () => {

      chrome.storage.local.get(
        ["blocked"],
        (data) => {

          let blocked =
            data.blocked || [];

          if (
            !blocked.includes(
              currentDomain
            )
          ) {

            blocked.push(
              currentDomain
            );

            chrome.storage.local.set(
              {
                blocked
              },
              () => {

                alert(
                  "Domain blocked successfully"
                );

              }
            );

          } else {

            alert(
              "Domain already blocked"
            );

          }

        }
      );

    }
  );