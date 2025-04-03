use aiprovider;

fn main() {
    let preset_parameters = aiprovider::Parameters::new();

    println!("{:?}", preset_parameters.preset.chat);
}
