// Constant variables for the models

// Meta-Llama
const LLAMA3_1_405B_INSTRUCT: &str = "meta-llama/Meta-Llama-3.1-405B-Instruct";
const LLAMA3_1_8B_INSTRUCT_TURBO: &str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo";
const LLAMA3_1_70B_INSTRUCT_TURBO: &str = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo";

// Deepseek
const DEEPSEEK_R1_TURBO: &str = "deepseek-ai/Deepseek-R1-Turbo";
const DEEPSEEK_R1: &str = "deepseek-ai/Deepseek-R1";
const DEEPSEEK_V3_0324: &str = "deepseek-ai/Deepseek-v3-0324";

// ======================================================================
// ====================== Struct for models =============================
// ======================================================================
// Meta-Llama
pub struct MetaLlama {
    pub llama3_1_405_instruct: &'static str,
    pub llama3_1_8b_instruct_turbo: &'static str,
    pub llama3_1_70b_instruct_turbo: &'static str,
}

impl Default for MetaLlama {
    fn default() -> Self {
        Self {
            llama3_1_405_instruct: LLAMA3_1_405B_INSTRUCT,
            llama3_1_8b_instruct_turbo: LLAMA3_1_8B_INSTRUCT_TURBO,
            llama3_1_70b_instruct_turbo: LLAMA3_1_70B_INSTRUCT_TURBO,
        }
    }
}

// Deepseek
pub struct Deepseek {
    pub r1_turbo: &'static str,
    pub r1: &'static str,
    pub v3_0324: &'static str,
}

impl Default for Deepseek {
    fn default() -> Self {
        Self {
            r1_turbo: DEEPSEEK_R1_TURBO,
            r1: DEEPSEEK_R1,
            v3_0324: DEEPSEEK_V3_0324,
        }
    }
}

// ======================================================================
// =================  put all models in here  ===========================
// ======================================================================
pub struct TextGenerationModels {
    pub meta_llama: MetaLlama,
    pub deepseek: Deepseek,
}

impl TextGenerationModels {
    pub fn new() -> Self {
        Self {
            meta_llama: MetaLlama::default(),
            deepseek: Deepseek::default(),
        }
    }
}
