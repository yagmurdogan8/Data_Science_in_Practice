# HaitiReportClassifier

**HaitiReportClassifier** is a machine learning project designed to classify unstructured situation reports from Haiti into structured outputs. The goal is to identify and extract key attributes such as:
- **Place**: The location of the event.
- **Perpetrator**: The individuals or groups involved.
- **Date**: When the event occurred.
- **Event Categories**: Whether the report involves gang violence, sexual violence, or famine.

## Features
- Fine-tuned NLP model based on [T5](https://huggingface.co/google/flan-t5-small).
- Structured classification of unstructured text.
- Multi-task classification approach with separate outputs for each attribute.
- Easily adaptable to other domains with similar classification needs.

## Usage
- First, run 
python fine_tune.py 
on your dataset, an example given as: extended_situation_reports.csv
- Then, run 
python classify.py 
on the fine-tuned model to classify new reports.