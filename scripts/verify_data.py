"""Script to verify data loading and validation."""
from src.dashboard.data_loader import Task1DataLoader
from src.utils.task1_validation import Task1Validator
from src.utils.logging_config import setup_logging

def main():
    logger = setup_logging()
    
    # Load data
    logger.info("Loading data...")
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Validate data
    logger.info("Validating data...")
    validator = Task1Validator(data['raw_data'])
    validation_results = validator.validate_task1_requirements()
    
    # Print validation results
    print("\nValidation Results:")
    for category, results in validation_results.items():
        print(f"\n{category.upper()}:")
        for item, is_valid in results.items():
            print(f"{item}: {'✓' if is_valid else '✗'}")

if __name__ == "__main__":
    main() 