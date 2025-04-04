mod chat_builder;
mod message;
mod preset_parameter;

use reqwest::{Client, ClientBuilder, Proxy};
use serde_json::{Value, json};
use std::collections::HashMap;

// export modules through this main module
pub use chat_builder::ChatBuilder;
pub use message::ChatBuilderMessage;
pub use preset_parameter::PresetParameter;

pub struct Api {
    pub api_key: &'static str,
    pub is_tor: bool,
    pub is_browser: bool,
    client: Client,
}
/// Main api handler
/// <div class="warning">This is a warning</div>
impl Api {
    pub fn new() -> Self {
        Self {
            api_key: "",
            is_tor: false,
            is_browser: false,
            client: ClientBuilder::new()
                .build()
                .expect("Failed to create client"),
        }
    }

    pub fn with_api_key(&mut self, api_key: &'static str) {
        self.api_key = api_key;
    }

    pub fn use_tor(&mut self) {
        self.is_tor = true;

        // setup client with tor
        self.client =
            ClientBuilder::new()
                .proxy(Proxy::all("socks5h://127.0.0.1:9050").expect(
                    "Failed to create proxy, have you imported `socks` features from reqwest?",
                ))
                .build()
                .expect("Failed to create client")
    }

    pub fn as_browser(&mut self) {
        self.is_browser = true;
    }

    pub async fn send_chat(&self, chat: &ChatBuilder, as_stream: bool) {
        // construct payload
        let mut payload: HashMap<&'static str, Value> = HashMap::new();
        payload.insert("model", json!(chat.model));
        payload.insert("messages", json!(chat.messages.clone()));
        for (param_key, param_value) in chat.parameters.value() {
            payload.insert(param_key, json!(param_value));
        }

        // add stream or not
        payload.insert("stream", json!(as_stream));

        let url: &str = "https://api.deepinfra.com/v1/openai/chat/completions";
        let mut client = self.client.post(url).json(&payload);

        // if simulating browser
        if self.is_browser {
            let browser_headers = Self::browser_header();
            for (key, value) in browser_headers {
                client = client.header(key, value);
            }

        // with api keys
        } else {
            client = client
                .header("Authorization", "Bearer ".to_string() + self.api_key)
                .header("Content-Type", "application/json");
        }

        let response = client.send().await.unwrap();

        // validate response

        if as_stream == false {
            // do normal response validation
            println!("{:#}", response.text().await.unwrap())
        } else {
            // do stream response validation
        }
    }

    pub fn send_tts(&self, model: &str, text: &str) {
        println!("{}", model);
        println!("{}", text);
    }

    // get headers as browser
    fn browser_header() -> HashMap<&'static str, &'static str> {
        let headers: HashMap<&str, &str> = HashMap::from([
            ("Content-Type", "application/json"),
            ("Host", "api.deepinfra.com"),
            ("Origin", "https://deepinfra.com"),
            ("Pragma", "no-cache"),
            ("Referer", "https://deepinfra.com/"),
            (
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36",
            ),
            ("Priority", "u=0"),
            ("Sec-Fetch-Dest", "empty"),
            ("Sec-Fetch-Mode", "cors"),
            ("Sec-Fetch-Site", "same-site"),
            ("X-Deepinfra-Source", "model-embed"),
        ]);
        headers
    }
}
