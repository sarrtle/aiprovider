use aiprovider::{Api, ChatBuilder, Models};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut api: Api = Api::new();
    api.as_browser();
    api.use_tor();

    let model = Models::new();
    let mut chat = ChatBuilder::new(model.text_generation.meta_llama.llama3_1_8b_instruct_turbo);

    chat.add_system_message("Be a helpful assistant");
    chat.add_user_message("Hello!");
    api.send_chat(&chat, false).await;

    Ok(())
}
