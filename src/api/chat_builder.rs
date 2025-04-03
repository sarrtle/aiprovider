// struct for chat builder
use crate::api::message::ChatBuilderMessage;
use crate::api::preset_parameter::Parameters;

pub struct ChatBuilder {
    model: &'static str,
    messages: Vec<ChatBuilderMessage>,
    parameters: Parameters,
}

impl ChatBuilder {
    pub fn new(model: &'static str) -> Self {
        Self {
            model,
            messages: Vec::new(),
            parameters: Parameters::new(),
        }
    }

    pub fn add_user_message(&mut self, message: ChatBuilderMessage) {
        self.messages.push(message);
    }

    pub fn add_assistant_message(&mut self, message: ChatBuilderMessage) {
        self.messages.push(message);
    }

    pub fn add_system_message(&mut self, message: ChatBuilderMessage) {
        self.messages.push(message);
    }

    pub fn set_parameters(&mut self, parameters: Parameters) {
        self.parameters = parameters;
    }

    pub fn set_model(&mut self, model: &'static str) {
        self.model = model;
    }
}
