import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, make_scorer


class ModeloML:
    def __init__(self, X, y):
        self.__X  = X
        self.__y = y

    def ver_outliers(self):
        plt.boxplot(self.__y)
        plt.title(f"Boxplot {self.__y.name}")
        plt.xlabel(self.__y.name)
        plt.ylabel("Valores")
        plt.show()

    def evaluar_modelos(self, models):
        tscv = TimeSeriesSplit(n_splits=5)

        results = {name: {"y_true": [], "y_pred": []} for name in models.keys()}

        for fold, (train_idx, test_idx) in enumerate(tscv.split(self.__X), 1):
            X_train, X_test = self.__X.iloc[train_idx], self.__X.iloc[test_idx]
            y_train, y_test = self.__y.iloc[train_idx], self.__y.iloc[test_idx]

            for name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                results[name]["y_true"].append(y_test)
                results[name]["y_pred"].append(pd.Series(y_pred, index=y_test.index))

        summary = {}
        for name, res in results.items():
            y_true_concat = pd.concat(res["y_true"])
            y_pred_concat = pd.concat(res["y_pred"])
            mae = mean_absolute_error(y_true_concat, y_pred_concat)
            rmse = root_mean_squared_error(y_true_concat, y_pred_concat)
            r2 = r2_score(y_true_concat, y_pred_concat)
            summary[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}

        print(pd.DataFrame(summary).T)


    def mejores_parametros(self, modelo):
        tscv = TimeSeriesSplit(n_splits=5)

        param_grid = {
            "n_estimators": [200, 400],
            "learning_rate": [0.05, 0.1],
            "max_depth": [4, 6]
        }

        grid = GridSearchCV(
            estimator=modelo,
            param_grid=param_grid,
            scoring=make_scorer(mean_absolute_error, greater_is_better=False),
            cv=tscv,
            verbose=2,
            n_jobs=-1
        )

        grid.fit(self.__X, self.__y)

        print("Mejores parametros:")
        print(grid.best_params_)
        print("\nMejor MAE:")
        print(-grid.best_score_)
        return grid.best_params_


    def entrenar_modelo(self, modelo):
        train_size = int(len(self.__X) * 0.8)

        X_train = self.__X.iloc[:train_size]
        y_train = self.__y.iloc[:train_size]

        X_test  = self.__X.iloc[train_size:]
        y_test  = self.__y.iloc[train_size:]

        modelo.fit(X_train, y_train)

        y_pred = modelo.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)

        print("MAE final:", mae)
        print("RMSE final:", rmse)
        return modelo

