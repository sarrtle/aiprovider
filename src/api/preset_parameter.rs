// struct for preset parameter

use std::collections::HashMap;

pub struct Preset {
    pub chat: HashMap<&'static str, &'static str>,
    pub coding: HashMap<&'static str, &'static str>,
    pub creative_story_telling: HashMap<&'static str, &'static str>,
}

impl Default for Preset {
    fn default() -> Self {
        let mut chat_map = HashMap::new();
        chat_map.insert("temperature", "0.7");
        chat_map.insert("top_p", "0.9");

        let mut coding_map = HashMap::new();
        coding_map.insert("temperature", "0.2");
        coding_map.insert("top_p", "1");
        coding_map.insert("frequency_penalty", "0.5");
        coding_map.insert("presence_penalty", "0.2");

        let mut creative_story_telling_map = HashMap::new();
        creative_story_telling_map.insert("temperature", "0.2");
        creative_story_telling_map.insert("top_p", "1");
        creative_story_telling_map.insert("frequency_penalty", "0.5");
        creative_story_telling_map.insert("presence_penalty", "0.2");

        Self {
            chat: chat_map,
            coding: coding_map,
            creative_story_telling: creative_story_telling_map,
        }
    }
}

pub struct Parameters {
    pub preset: Preset,
}

impl Parameters {
    pub fn new() -> Self {
        Self {
            preset: Preset::default(),
        }
    }
}
