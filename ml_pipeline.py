import numpy as np
from scipy import stats
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
)

# базовая модель
model_a = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)
model_a.fit(X_train, y_train)
y_pred = model_a.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy RandomForestClassifier: {accuracy:.2f}")

# новая модель для A/B-теста
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_b = LogisticRegression(
    random_state=42,
    C=0.1,
)
model_b.fit(X_train_scaled, y_train)
y_pred = model_b.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy LogisticRegression: {accuracy:.2f}")

# A/B-тестирование
accuracy_a = []
accuracy_b = []
for _ in range(1000):
    idx = np.random.choice(len(y_test), size=len(y_test), replace=True)
    
    pred_a = model_a.predict(X_test[idx])
    pred_b = model_b.predict(X_test_scaled[idx])
    
    accuracy_a.append(accuracy_score(y_test[idx], pred_a))
    accuracy_b.append(accuracy_score(y_test[idx], pred_b))

t_stat, p_value = stats.mannwhitneyu(accuracy_a, accuracy_b)

print(f"\nModel A (RandomForest): {np.mean(accuracy_a):.2f} ± {np.std(accuracy_a):.2f}")
print(f"Model B (LogisticRegression): {np.mean(accuracy_b):.2f} ± {np.std(accuracy_b):.2f}")
print(f"p-value: {p_value:.2e}")

alpha = 0.05

if p_value < alpha:
    print(
        f"\nПоскольку P-значение ({p_value:.2e}) меньше уровня значимости ({alpha}), мы отвергаем нулевую гипотезу.\n"
        "Существует статистически значимая разница между точностью Модели A и Модели B.\n"
        f"Выбираем модель {'A' if np.mean(accuracy_a) > np.mean(accuracy_b) else 'B'}"
    )

else:
    print(
        f"\nПоскольку P-значение ({p_value:.2e}) больше уровня значимости ({alpha}), "
        "мы не можем отвергнуть нулевую гипотезу.\n"
        "Нет статистически значимой разницы между точностью Модели A и Модели B."
    )
