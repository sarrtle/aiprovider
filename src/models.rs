mod reasoning;
mod text_generation;
mod tts;
mod vision;

use reasoning::ReasoningModels;
use text_generation::TextGenerationModels;
use tts::TTSModels;
use vision::VisionModels;

pub struct Models {
    pub text_generation: TextGenerationModels,
    pub reasoning_text_generation: ReasoningModels,
    pub vision_text_generation: VisionModels,
    pub tts: TTSModels,
}

impl Models {
    pub fn new() -> Self {
        Self {
            text_generation: TextGenerationModels::new(),
            reasoning_text_generation: ReasoningModels::new(),
            vision_text_generation: VisionModels::new(),
            tts: TTSModels::new(),
        }
    }
}
