from collections import Counter
from math import sqrt


DEFAULT_SAMPLES = [
    ([1.0, 1.2, 1.1], "class_0"),
    ([1.4, 1.0, 1.3], "class_0"),
    ([0.8, 1.5, 1.0], "class_0"),
    ([4.8, 5.1, 5.0], "class_1"),
    ([5.2, 4.7, 5.4], "class_1"),
    ([4.5, 5.4, 4.8], "class_1"),
    ([8.8, 9.0, 8.7], "class_2"),
    ([9.3, 8.6, 9.1], "class_2"),
    ([8.5, 9.4, 9.0], "class_2"),
]


class StandardScaler:
    def __init__(self) -> None:
        self.means: list[float] = []
        self.scales: list[float] = []

    def fit(self, samples: list[list[float]]) -> None:
        feature_count = len(samples[0])
        self.means = [sum(row[i] for row in samples) / len(samples) for i in range(feature_count)]
        self.scales = []
        for i, mean in enumerate(self.means):
            variance = sum((row[i] - mean) ** 2 for row in samples) / len(samples)
            self.scales.append(sqrt(variance) or 1.0)

    def transform(self, samples: list[list[float]]) -> list[list[float]]:
        return [
            [(value - mean) / scale for value, mean, scale in zip(row, self.means, self.scales)]
            for row in samples
        ]


class KNNModel:
    def __init__(self, k: int = 5) -> None:
        if k < 1 or k % 2 == 0:
            raise ValueError("k must be a positive odd number")
        self.k = k
        self._samples: list[list[float]] = []
        self._labels: list[str] = []
        self._scaler = StandardScaler()

    @property
    def is_ready(self) -> bool:
        return bool(self._samples)

    def fit(self, samples: list[list[float]], labels: list[str]) -> None:
        if not samples or len(samples) != len(labels):
            raise ValueError("samples and labels must be non-empty and have equal length")
        feature_count = len(samples[0])
        if feature_count != 3 or any(len(row) != feature_count for row in samples):
            raise ValueError("each sample must contain exactly 3 numeric features")
        self._scaler.fit(samples)
        self._samples = self._scaler.transform(samples)
        self._labels = labels

    def fit_default_data(self) -> None:
        samples, labels = zip(*DEFAULT_SAMPLES)
        self.fit(list(samples), list(labels))

    def predict(self, features: list[float]) -> str:
        if not self.is_ready:
            raise RuntimeError("model has not been fitted")
        if len(features) != 3:
            raise ValueError("features must contain exactly 3 values")
        normalized = self._scaler.transform([features])[0]
        distances = sorted(
            (self._distance(normalized, sample), label)
            for sample, label in zip(self._samples, self._labels)
        )
        nearest_labels = [label for _, label in distances[: min(self.k, len(distances))]]
        return Counter(nearest_labels).most_common(1)[0][0]

    @staticmethod
    def _distance(left: list[float], right: list[float]) -> float:
        return sqrt(sum((left_value - right_value) ** 2 for left_value, right_value in zip(left, right)))
