from src.networksecurity.entity import ModelTrainerConfig
from src.networksecurity import logger
from sklearn.metrics import r2_score, accuracy_score
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,RandomForestClassifier)
from sklearn.linear_model import LogisticRegression
from src.networksecurity import constants as const
from src.networksecurity.utils.common import load_numpy_array_data, load_object, save_object
import mlflow
import dagshub
from sklearn.model_selection import GridSearchCV
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
from sklearn.metrics import f1_score,precision_score,recall_score

class ModelTrainer:
    def __init__(self, config = ModelTrainerConfig):
        logger.info("Initialized ModelTrainer")
        self.config = config
        self.train_data = load_numpy_array_data(self.config.train_npy)
        self.test_data = load_numpy_array_data(self.config.test_npy)
    
    def track_mlflow(self,model_name, y_test, y_pred):
        try:
            logger.info("Inside track_mlfow method")
            load_dotenv()
            dagshub.init(repo_owner='bsaarun54', repo_name='networksecurity', mlflow=True)
            mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URL'])
            mlflow.set_experiment("network_security_experiments")
            with mlflow.start_run():
                mlflow.log_param("Best model name", model_name)
                model_f1_score = f1_score(y_pred=y_pred, y_true=y_test)
                mlflow.log_metric('fi_score', model_f1_score)
                precision = precision_score(y_pred=y_pred, y_true=y_test)
                mlflow.log_metric('precision',precision)
                model_recall_score = recall_score(y_pred=y_pred, y_true=y_test)
                mlflow.log_metric('recall_score', model_recall_score)



        except Exception as e:
            logger.error(f"Error occured inside track_mlflow:{e}")
            raise e


    def evaluate_models(self, X_train,y_train,X_test,y_test,models,params):
        try:
            logger.info("Inside evaluate_model method")
            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]
                param = params[list(models.keys())[i]]
                gs = GridSearchCV(model, param, cv=3)
                gs.fit(X_train,y_train)
                model_name = type(gs.best_estimator_).__name__
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                test_model_score = r2_score(y_test, y_pred)

                # track in mlflow
                if const.ENV_DAGSHUB == 'Y':
                    self.track_mlflow(model_name, y_test, y_pred)
                else:
                    logger.info("ENV_DAGSHUB is N, not logging experiments")

                report[list(models.keys())[i]] = [test_model_score, gs.best_params_]
            return report


        except Exception as e:
            logger.error(f"error occured inside evaluate_model:{e}")
            raise e

    def train_model(self, X_train, y_train, X_test, y_test):
        try: 
            logger.info("Inside train_model method")
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Adaboost": AdaBoostClassifier(),
                "Logistic Regression": LogisticRegression(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1)
            }
            params= {
                "Random Forest":{
                    "n_estimators" : [8,16,32,64,128],
                    "criterion" : ["gini","entropy"]
                },
                "Adaboost":{
                    "learning_rate":[0.1,0.01,0.001],
                    'n_estimators':[8,16,32,64,128]

                },
                "Logistic Regression":{},
                "Gradient Boosting":{
                    "learning_rate":[0.1,0.01,0.001],
                    'n_estimators':[8,16,32,64,128]
                }
            }

            model_report:dict=self.evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)
            best_model_score = max(sorted(model_report.values()))
            logger.info(f"Best model score: {best_model_score}")
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            logger.info(f"Best model name:{best_model_name}")
            best_model_params = model_report.get(best_model_name)[1]
            logger.info(f"Best model params: {best_model_params}")

            best_model = models.get(best_model_name)
            best_model.set_params(**best_model_params)
            best_model.fit(X_train, y_train)

            y_pred = best_model.predict(X_test)
            acc_score = accuracy_score(y_pred=y_pred, y_true=y_test)
            logger.info(f"{best_model_name} is {acc_score} accurate")

            
            logger.info("saving the best model in artifacts")
            save_object(self.config.model_name, best_model)
            logger.info("saving the model in data folder for s3 sync")
            save_object(const.FINAL_MODEL, best_model)

        except Exception as e:
            logger.error(f"Error occured inside train_model:{e}")
            raise e

    def initiate_model_trainer(self):
        try:
            logger.info("Inside initiate_model_trainer method")
            X_train, y_train, X_test, y_test = (self.train_data[:,:-1], self.train_data[:,-1],
                                            self.test_data[:,:-1], self.test_data[:,-1])
            best_model = self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            logger.error(f"error occured inside initiate_model_trainer:{e}")
            raise e
