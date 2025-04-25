from ultralytics import YOLO
import torch
import multiprocessing

def train_model():
    # Check if CUDA (GPU) is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🔄 Using device: {device.upper()}")

    # Load a pre-trained YOLOv8 model for better convergence
    model = YOLO("yolov8s.pt")

    # Train with optimized hyperparameters
    model.train(
        data="data.yaml",         # Ensure dataset is correctly formatted
        epochs=100,               # Train longer for better convergence
        batch=8,                 # Increase batch size if GPU allows
        imgsz=1280,               # Higher resolution improves small object detection
        patience=50,              # Early stopping patience
        optimizer="AdamW",        # Better weight updates
        lr0=0.0005,               # Lower learning rate for stability
        lrf=0.01,                 # Final learning rate
        weight_decay=0.0005,      # Helps prevent overfitting
        warmup_epochs=3,          # Warmup to stabilize training
        cos_lr=True,              # Cosine learning rate scheduler
        dropout=0.2,              # Add dropout for regularization

        # Data Augmentations
        hsv_h=0.02, hsv_s=0.8, hsv_v=0.4,  # Color jitter
        flipud=0.5, fliplr=0.5,            # Flip images
        mosaic=1.0, mixup=0.2,             # Advanced augmentations
        degrees=10, shear=5, scale=0.5,

        # Validation & Logging
        val=True,                # Perform validation
        device=device,           # Train on GPU if available
        project="runs/train",    # Save training result
        verbose=True             # Print more training info
    )

    print("✅ Training completed. Best model saved!")

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Required for Windows compatibility
    train_model()

