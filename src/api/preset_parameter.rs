// struct for preset parameter

use std::collections::HashMap;

pub enum PresetParameter {
    Chat,
    Coding,
    CreativeStoryTelling,
}

impl PresetParameter {
    pub fn value(&self) -> HashMap<&'static str, f32> {
        match self {
            PresetParameter::Chat => {
                let mut map = HashMap::new();
                map.insert("temperature", 0.7);
                map.insert("top_p", 0.9);
                map
            }
            PresetParameter::Coding => {
                let mut map = HashMap::new();
                map.insert("temperature", 0.2);
                map.insert("top_p", 1.0);
                map.insert("frequency_penalty", 0.5);
                map.insert("presence_penalty", 0.2);
                map
            }
            PresetParameter::CreativeStoryTelling => {
                let mut map = HashMap::new();
                map.insert("temperature", 1.2);
                map.insert("top_p", 0.5);
                map.insert("frequency_penalty", 1.2);
                map.insert("presence_penalty", 0.5);
                map
            }
        }
    }
}
