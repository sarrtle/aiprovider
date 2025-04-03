// all reasoning text generation models

// Constant variables for the models

const QWQ_32B: &str = "Qwen/QwQ-32B";

// ======================================================================
// ====================== Struct for models =============================
// ======================================================================
// Qwen
pub struct Qwen {
    pub qwq_32b: &'static str,
}

impl Qwen {
    pub fn new() -> Self {
        Self { qwq_32b: QWQ_32B }
    }
}

// ======================================================================
// ==================  put all models in here  ===========================
// ======================================================================
pub struct ReasoningModels {
    pub qwen: Qwen,
}

impl ReasoningModels {
    pub fn new() -> Self {
        Self { qwen: Qwen::new() }
    }
}
