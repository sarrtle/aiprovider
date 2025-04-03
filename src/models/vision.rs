// all vision text generation models

// Constant variables for the models

// Google
const GEMMA_3_27B_IT: &str = "google/gemma-3-27b-it";

// Meta-Llama
const LLAMA3_2_90B_VISION_INSTRUCT: &str = "meta-llama/Llama-3.2-90B-Vision-Instruct";

// ======================================================================
// ====================== Struct for models =============================
// ======================================================================
// Google
pub struct Google {
    pub gemma_3_27_b_it: &'static str,
}
impl Default for Google {
    fn default() -> Self {
        Self {
            gemma_3_27_b_it: GEMMA_3_27B_IT,
        }
    }
}

// Meta-Llama
pub struct MetaLlama {
    pub llama3_2_90b_vision_instruct: &'static str,
}
impl Default for MetaLlama {
    fn default() -> Self {
        Self {
            llama3_2_90b_vision_instruct: LLAMA3_2_90B_VISION_INSTRUCT,
        }
    }
}

// ======================================================================
// ======================= put all models in here  ======================
// ======================================================================

pub struct VisionModels {
    pub google: Google,
    pub meta_llama: MetaLlama,
}

impl VisionModels {
    pub fn new() -> Self {
        Self {
            google: Google::default(),
            meta_llama: MetaLlama::default(),
        }
    }
}
