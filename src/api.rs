mod chat_builder;
mod message;
mod preset_parameter;

// export modules through this main module
pub use chat_builder::ChatBuilder;
pub use message::ChatBuilderMessage;
pub use preset_parameter::Parameters;

pub struct Api {
    api_key: &'static str,
    use_tor: bool,
}

/// Main api handler
/// <div class="warning">This is a warning</div>
impl Api {
    pub fn new(api_key: &'static str, use_tor: bool) -> Self {
        Self { api_key, use_tor }
    }

    pub fn send_chat(&self, chat: &mut ChatBuilder) {
        println!("{}", self.use_tor);
        println!("{}", self.api_key);
        chat.set_model("Something else");
    }

    pub fn send_tts(&self, model: &str, text: &str) {
        println!("{}", model);
        println!("{}", text);
    }
}
