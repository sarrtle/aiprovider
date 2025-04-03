// all text to speech models

// Constant variables for the models

// Sesame
const SESAME: &str = "sesame/csm-1b";

// Hexgrad
const KOKORO: &str = "hexgrad/Kokoro-82M";

// Zyphra
const ZYPRA_HYBRID: &str = "Zypra/Zonos-v0.1-hybrid";
const ZYPRA_TRANSFORMER: &str = "Zypra/Zonos-v0.1-transformer";

// ======================================================================
// ====================== Struct for models =============================
// ======================================================================
// Sesame
pub struct Sesame {
    pub csm_1b: &'static str,
}
impl Default for Sesame {
    fn default() -> Self {
        Self { csm_1b: SESAME }
    }
}

// Hexgrad
pub struct Hexgrad {
    pub kokoro_82m: &'static str,
}
impl Default for Hexgrad {
    fn default() -> Self {
        Self { kokoro_82m: KOKORO }
    }
}

// Zyphra
pub struct Zyphra {
    pub zonos_v0_1_hybrid: &'static str,
    pub zonos_v0_1_transformer: &'static str,
}
impl Default for Zyphra {
    fn default() -> Self {
        Self {
            zonos_v0_1_hybrid: ZYPRA_HYBRID,
            zonos_v0_1_transformer: ZYPRA_TRANSFORMER,
        }
    }
}

// ======================================================================
// ======================= put all models in here  ======================
// ======================================================================
pub struct TTSModels {
    pub sesame: Sesame,
    pub hexgrad: Hexgrad,
    pub zyphra: Zyphra,
}
impl TTSModels {
    pub fn new() -> Self {
        Self {
            sesame: Sesame::default(),
            hexgrad: Hexgrad::default(),
            zyphra: Zyphra::default(),
        }
    }
}
