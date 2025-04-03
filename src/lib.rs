//! A rust wrapper for a certain API provider.
//!
//! [Can handle chat, text to speech and vision]

mod api;
mod models;

// models
pub use models::Models;

// api
pub use api::Api;
pub use api::ChatBuilder;
pub use api::ChatBuilderMessage;
pub use api::Parameters;
