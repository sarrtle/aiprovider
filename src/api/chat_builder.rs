use std::collections::HashMap;

// struct for chat builder
use crate::api::message::{ChatBuilderMessage, Role};
use crate::api::preset_parameter::PresetParameter;

pub struct ChatBuilder {
    pub model: &'static str,
    pub messages: Vec<HashMap<&'static str, &'static str>>,
    pub parameters: PresetParameter,
}

/// Create a chat builder
/// # Arguments
/// - `model` - The model to use
/// - `messages` - The messages to send
/// - `parameters` - The parameters to use
impl ChatBuilder {
    pub fn new(model: &'static str) -> Self {
        Self {
            model,
            messages: Vec::new(),
            parameters: PresetParameter::Chat,
        }
    }

    pub fn add_user_message(&mut self, message: &'static str) {
        let message = ChatBuilderMessage::new(Role::User, message);
        self.messages.push(message.as_hashmap());
    }

    pub fn add_assistant_message(&mut self, message: &'static str) {
        let message = ChatBuilderMessage::new(Role::Assistant, message);
        self.messages.push(message.as_hashmap());
    }

    pub fn add_system_message(&mut self, message: &'static str) {
        let message = ChatBuilderMessage::new(Role::System, message);
        self.messages.push(message.as_hashmap());
    }

    pub fn set_parameters(&mut self, parameters: PresetParameter) {
        self.parameters = parameters;
    }

    pub fn set_model(&mut self, model: &'static str) {
        self.model = model;
    }
}
