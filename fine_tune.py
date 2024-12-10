from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer

def main():
    # Step 1: Load the CSV file and prepare the dataset
    csv_file_path = "extended_situation_reports.csv"  # Update with your local file path
    dataset = load_dataset("csv", data_files=csv_file_path, delimiter=",")  # Ensure the correct delimiter is used

    # Verify column names
    print("Dataset column names:", dataset['train'].column_names)

    # Define the preprocessing function
    def preprocess_data(example):
        example['input_text'] = f"Classify: {example['Text']}"
        example['target_text'] = (
            f"Place: {example['Place']}\n"
            f"Perpetrator: {example['Perpetrator']}\n"
            f"Date: {example['Date']}\n"
            f"Gang violence: {example['Gang violence']}\n"
            f"Sexual violence: {example['Sexual violence']}\n"
            f"Famine: {example['Famine']}"
        )
        return example

    # Preprocess the dataset
    processed_dataset = dataset.map(preprocess_data)

    # Step 2: Split the dataset into train and validation sets
    train_test_split = processed_dataset['train'].train_test_split(test_size=0.2)
    train_dataset = train_test_split['train']
    validation_dataset = train_test_split['test']

    # Step 3: Tokenize the dataset
    model_name = "google/flan-t5-small"  # Smaller model for faster fine-tuning
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_data(example):
        tokenized_input = tokenizer(example['input_text'], truncation=True, padding="max_length", max_length=256)
        tokenized_target = tokenizer(example['target_text'], truncation=True, padding="max_length", max_length=256)
        return {
            "input_ids": tokenized_input['input_ids'],
            "attention_mask": tokenized_input['attention_mask'],
            "labels": tokenized_target['input_ids']
        }

    tokenized_train_dataset = train_dataset.map(tokenize_data, batched=True)
    tokenized_validation_dataset = validation_dataset.map(tokenize_data, batched=True)

    # Step 4: Define training arguments with optimizations
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        evaluation_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=1,  # Smaller batch size
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,  # Simulate a larger batch size
        num_train_epochs=5,  # Fewer epochs to save time
        weight_decay=0.01,
        save_strategy="epoch",
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=50,
        report_to="none",
        fp16=True,  # Enable mixed precision training
        dataloader_num_workers=0,  # Use single-threaded data loading on Windows
        disable_tqdm=False  # Show progress bars
    )

    # Step 5: Fine-tune the model
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_validation_dataset
    )

    print("Starting training...")
    trainer.train()
    print("Training completed.")

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")

if __name__ == "__main__":
    main()
