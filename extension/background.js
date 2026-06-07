chrome.runtime.onMessage.addListener(

  async (
    message,
    sender
  ) => {

    if (
      message.action !==
      "scanURL"
    ) {
      return;
    }

    try {

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
              url: message.url
            })
          }
        );

      const result =
        await response.json();

      chrome.tabs.sendMessage(

        sender.tab.id,

        {
          action: "scanResult",
          result: result
        }

      );

    } catch (error) {

      console.error(error);

    }

  }

);