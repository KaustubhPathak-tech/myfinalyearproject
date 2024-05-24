import numpy as np

# Create synthetic time series:
def trend(time, slope=0):
    return slope * time

def emergency(season_time):
    """Just an arbitrary pattern; you can change it if you wish."""
    return np.where(season_time < 0.4, np.cos(season_time * 2 * np.pi), 1 / np.exp(3 * season_time))

def seasonality(time, period, amplitude=1, phase=0):
    """Repeats the same pattern in each period."""
    season_time = ((time + phase) % period) / period
    return amplitude * emergency(season_time)

def white_noise(time, noise_level=1, seed=None):
    return np.random.RandomState(seed).randn(len(time)) * noise_level

time = np.arange(4 * 365 + 1) # 1 is added since every four years there is a leap year.
baseline = 10
slope = 0.05
amplitude = 50
series = baseline + trend(time, slope) + seasonality(time, period=365, amplitude=amplitude)
noise_level = 5
noise = white_noise(time, noise_level, seed=42)
series += noise

# Define training & validation periods:
split_time = 1000
x_train = series[:split_time]
x_valid = series[split_time:]

# Create custom `Dataset` class; it'll be used by the `model_forecast` function below:
import torch
from torch.utils.data import Dataset, DataLoader

class WindowDataset(Dataset):
    def __init__(self, series, window_size):
        window_size += 1
        self.windows = []
        for i in range(0, len(series) - window_size + 1, 1):
            self.windows.append(series[i:i + window_size])

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        window = self.windows[idx]
        return window[:-1], window[-1]

# Re-create model & load weights:
import torch.nn as nn
from huggingface_hub import PyTorchModelHubMixin

device = torch.device("cpu")

class LinearModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, window_size):
        super().__init__()
        self.linear = nn.Linear(window_size, 1)

    def forward(self, x):
        return self.linear(x)

window_size = 30
model = LinearModel.from_pretrained("/linear-regression-geron-time-series", window_size=window_size)
model.to(device)

# Forecast on validation period:
def model_forecast(model, series):
    series = torch.tensor(series, dtype=torch.float32)
    ds = WindowDataset(series, window_size)
    dl = DataLoader(ds, batch_size=32, shuffle=False)
    forecast = []
    for x_batch, y_batch in dl:
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)
        with torch.no_grad():
            preds = model(x_batch)
        forecast.append(preds.squeeze())
    forecast = torch.cat(forecast)
    return forecast.cpu().numpy()

linear_forecast = model_forecast(model, series[split_time - window_size:])
