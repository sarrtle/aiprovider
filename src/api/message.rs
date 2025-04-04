// Message struc

use std::collections::HashMap;

pub enum Role {
    User,
    Assistant,
    System,
}

impl Role {
    pub fn as_str(&self) -> &'static str {
        match self {
            Role::User => "user",
            Role::Assistant => "assistant",
            Role::System => "system",
        }
    }
}

pub struct ChatBuilderMessage {
    pub role: Role,
    pub content: &'static str,
}

impl ChatBuilderMessage {
    pub fn new(role: Role, content: &'static str) -> Self {
        Self { role, content }
    }

    pub fn as_hashmap(&self) -> HashMap<&'static str, &'static str> {
        let mut map = HashMap::new();
        map.insert("role", self.role.as_str());
        map.insert("content", &self.content);
        map
    }
}
