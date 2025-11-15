"""
Training script for fine-tuning multilingual toxicity detection model

This script helps you fine-tune a multilingual model on your Kannada/Hindi data.

Requirements:
- Training data in CSV format with columns: 'text', 'label' (0=non-toxic, 1=toxic)
- Or JSON format: [{"text": "...", "label": 0/1}, ...]

Usage:
    python train_multilingual.py --data data.csv --output_dir ./models --epochs 3
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from datasets import Dataset
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np

def load_data(file_path: str, format: str = "csv"):
    """Load training data from file"""
    if format == "csv":
        df = pd.read_csv(file_path)
        # Expected columns: 'text', 'label'
        texts = df['text'].tolist()
        labels = df['label'].tolist()
    elif format == "json":
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        texts = [item['text'] for item in data]
        labels = [item['label'] for item in data]
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return texts, labels

def preprocess_data(texts: list, labels: list, tokenizer, max_length: int = 512):
    """Preprocess data for training"""
    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt"
    )
    
    # Convert to dataset format
    dataset = Dataset.from_dict({
        'input_ids': encodings['input_ids'],
        'attention_mask': encodings['attention_mask'],
        'labels': labels
    })
    
    return dataset

def compute_metrics(eval_pred):
    """Compute metrics for evaluation"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
    accuracy = accuracy_score(labels, predictions)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def train_model(
    data_path: str,
    output_dir: str = "./models",
    model_name: str = "xlm-roberta-base",
    epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    train_size: float = 0.8,
    format: str = "csv"
):
    """Train multilingual toxicity detection model"""
    
    print(f"Loading data from {data_path}...")
    texts, labels = load_data(data_path, format=format)
    
    print(f"Loaded {len(texts)} examples")
    print(f"Labels distribution: {pd.Series(labels).value_counts().to_dict()}")
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=1-train_size, random_state=42, stratify=labels
    )
    
    print(f"Train examples: {len(train_texts)}")
    print(f"Validation examples: {len(val_texts)}")
    
    # Load tokenizer and model
    print(f"Loading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2  # toxic, non-toxic
    )
    
    # Preprocess data
    print("Preprocessing data...")
    train_dataset = preprocess_data(train_texts, train_labels, tokenizer)
    val_dataset = preprocess_data(val_texts, val_labels, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{output_dir}/logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
    )
    
    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save model
    print(f"Saving model to {output_dir}...")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    # Evaluate
    print("Evaluating model...")
    eval_results = trainer.evaluate()
    print(f"Evaluation results: {eval_results}")
    
    print("Training completed!")
    print(f"Model saved to: {output_dir}")
    print(f"Best F1 score: {eval_results.get('eval_f1', 0.0):.4f}")

def main():
    parser = argparse.ArgumentParser(description="Train multilingual toxicity detection model")
    parser.add_argument("--data", type=str, required=True, help="Path to training data file")
    parser.add_argument("--output_dir", type=str, default="./models", help="Output directory for model")
    parser.add_argument("--model_name", type=str, default="xlm-roberta-base", help="Base model name")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--train_size", type=float, default=0.8, help="Training set size ratio")
    parser.add_argument("--format", type=str, default="csv", choices=["csv", "json"], help="Data format")
    
    args = parser.parse_args()
    
    train_model(
        data_path=args.data,
        output_dir=args.output_dir,
        model_name=args.model_name,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        train_size=args.train_size,
        format=args.format
    )

if __name__ == "__main__":
    main()

