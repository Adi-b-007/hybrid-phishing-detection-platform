chrome.runtime.sendMessage({

  action: "scanURL",

  url: window.location.href

});

chrome.runtime.onMessage.addListener(

  (message) => {

    if (
      message.action !==
      "scanResult"
    ) {
      return;
    }

    const result =
      message.result;

    if (
      result.prediction ===
      "Legitimate"
    ) {

      showSafeBanner(
        result.confidence
      );

    } else {

      showWarningScreen(
        result
      );

    }

  }

);

function showSafeBanner(
  confidence
) {

  const banner =
    document.createElement(
      "div"
    );

  banner.innerHTML = `
    🛡 Safe Website
    <br>
    Confidence:
    ${confidence}%
  `;

  banner.style.cssText = `
    position:fixed;
    top:20px;
    right:20px;
    background:#00aa55;
    color:white;
    padding:15px;
    border-radius:10px;
    z-index:999999;
    font-weight:bold;
  `;

  document.body.appendChild(
    banner
  );

  setTimeout(
    () => banner.remove(),
    4000
  );

}

function showWarningScreen(
  result
) {

  const overlay =
    document.createElement(
      "div"
    );

  overlay.style.cssText = `
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:#111;
    color:white;
    z-index:999999;
    display:flex;
    justify-content:center;
    align-items:center;
  `;

  overlay.innerHTML = `
    <div style="
      width:700px;
      text-align:center;
    ">

      <h1 style="
        color:red;
      ">
      ⚠ SECURITY WARNING
      </h1>

      <h2>
      Confidence:
      ${result.confidence}%
      </h2>

      <h3>
      Why Suspicious?
      </h3>

      ${
        result.reasons
        .map(
          reason =>
          `<p>• ${reason}</p>`
        )
        .join("")
      }

      <br>

      <button
        id="continueBtn"
      >
      Continue Anyway
      </button>

      <button
        id="blockBtn"
      >
      Go Back
      </button>

    </div>
  `;

  document.body.appendChild(
    overlay
  );

  document
  .getElementById(
    "continueBtn"
  )
  .onclick = () => {

    overlay.remove();

  };

  document
  .getElementById(
    "blockBtn"
  )
  .onclick = () => {

    window.history.back();

  };

}