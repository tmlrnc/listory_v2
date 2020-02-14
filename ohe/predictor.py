import csv

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from ohe.config import get_ohe_config


class OneHotPredictor(object):

    def get_accuracy(self,y_pred_one_hot, y_test, test_len):
        correct = 0
        y_pred_one_hot_list = list(y_pred_one_hot)
        y_test_list = list(y_test)
        for i in range(test_len):
            if y_pred_one_hot_list[i] == y_test_list[i]:
                correct = correct + 1
        return ((correct / test_len) * 100)

    def get_best_accuracy(self,y_pred_one_hot, y_test, test_len):
        correct = 0
        y_pred_one_hot_list = list(y_pred_one_hot)
        y_test_list = list(y_test)
        for i in range(test_len):
            if y_pred_one_hot_list[i] == y_test_list[i]:
                correct = correct + 1
        return ((correct / test_len) * 100)

    def __init__(self, target,predict_list,training_test_split_percent):
        self.target = target
        self.predict_list = predict_list
        self.training_test_split_percent = int(training_test_split_percent)
        self.accuracy_list = []
        self.g_acc = -1
        self.s_acc = -1
        self.l_acc = -1
        self.r_acc = -1
        self.mlp_acc = -1





        return


    def predict_GaussianNB(self):
        from sklearn.preprocessing import LabelEncoder
        self.labelencoder = LabelEncoder()
        self.X_train_label = self.X_train_ordinal
        self.X_test_label = self.X_test_ordinal
        for i in range(self.col_len):
            self.X_train_label[:, i] = self.labelencoder.fit_transform(self.X_train_label[:, i])
            self.X_test_label[:, i] = self.labelencoder.fit_transform(self.X_test_label[:,i])
        self.gnb = GaussianNB()
        self.y_pred_one_hot_g = self.gnb.fit(self.X_train_label, self.y_train).predict(self.X_test_label)
        self.g_acc = self.get_accuracy(self.y_pred_one_hot_s, self.y_test, self.test_len)
        self.accuracy_list.append(self.g_acc)


    def predict_MLPClassifier(self):
        self.mlp = MLPClassifier(solver=get_ohe_config().MLP_solver, alpha=get_ohe_config().MLP_alpha,
                                 hidden_layer_sizes=(get_ohe_config().MLP_layers, get_ohe_config().MLP_neurons),
                                 random_state=get_ohe_config().MLP_random_state)
        self.mlp.fit(self.X_train_one_hot, self.y_train)


        self.l.fit(self.X_train_one_hot, self.y_train)
        self.y_pred_one_hot_mlp = list(self.mlp.predict(self.X_test_one_hot))
        self.mlp_acc = self.get_accuracy(self.y_pred_one_hot_mlp, self.y_test, self.test_len)
        self.accuracy_list.append(self.mlp_acc)


    def predict_LR(self):
        self.l = LogisticRegression(random_state=get_ohe_config().LR_random_state)
        self.l.fit(self.X_train_one_hot, self.y_train)
        self.y_pred_one_hot_l = list(self.l.predict(self.X_test_one_hot))
        self.l_acc = self.get_accuracy(self.y_pred_one_hot_l, self.y_test, self.test_len)
        self.accuracy_list.append(self.l_acc)


    def predict_RF(self):
        self.r = RandomForestClassifier(n_estimators=get_ohe_config().RF_n_estimators,
                                        max_depth=get_ohe_config().RF_max_depth)
        self.r.fit(self.X_train_one_hot, self.y_train)
        self.y_pred_one_hot_r = self.r.predict(self.X_test_one_hot)
        self.r_acc = self.get_accuracy(self.y_pred_one_hot_r, self.y_test, self.test_len)
        self.accuracy_list.append(self.r_acc)


    def predict_SVM(self):
        self.s = svm.LinearSVC(random_state=get_ohe_config().SVM_random_state)
        self.s.fit(self.X_train_one_hot, self.y_train)
        self.y_pred_one_hot_s = self.s.predict(self.X_test_one_hot)
        self.s_acc = self.get_accuracy(self.y_pred_one_hot_s, self.y_test, self.test_len)
        self.accuracy_list.append(self.s_acc)


    def predict(self, one_hot_encode_object, features, target):
        self.csv_column_name_list = []
        for col in features:
            if col != self.target:
                self.csv_column_name_list.append(col)

        self.train = one_hot_encode_object
        self.train.columns = features

        self.Y = self.train[target]
        mylen = self.Y.size
        SP = self.training_test_split_percent/100
        train_len = int(round(mylen * SP))
        train_list = []
        train_list.append(self.csv_column_name_list)
        self.col_len = len(self.csv_column_name_list)

        self.X = self.train[self.csv_column_name_list]
        self.test_len = mylen - train_len

        self.X_train = self.X.iloc[:train_len]
        self.X_test = self.X.iloc[train_len:]
        self.y_train = self.Y.iloc[:train_len]
        self.y_test = self.Y.iloc[train_len:]

        self.X_train_ordinal = self.X_train.values
        self.X_test_ordinal = self.X_test.values
        self.s = svm.LinearSVC()

        from sklearn.preprocessing import OneHotEncoder
        self.enc = OneHotEncoder(handle_unknown='ignore')
        self.enc.fit(self.X_train_ordinal)

        self.X_train_one_hot = self.enc.transform(self.X_train_ordinal)
        self.X_test_one_hot = self.enc.transform(self.X_test_ordinal)


        if "LR" in self.predict_list: self.predict_LR()
        if "RF" in self.predict_list: self.predict_RF()
        if "SVM" in self.predict_list: self.predict_SVM()
        if "GNB" in self.predict_list: self.predict_GaussianNB()
        if "MLP" in self.predict_list: self.predict_MLPClassifier()



        return



    def write_predict_csv(self,file_out_name):
        self.y_test_list = list(self.y_test)
        my_header = []
        my_accuracy = []
        if "LR" in self.predict_list:
            if self.l_acc >= max(self.accuracy_list):
                my_header.append('Logical Regression: MODEL SELECTED')
            else:
                my_header.append('Logical Regression')
            my_accuracy.append('LR Accuracy: ' + str(self.l_acc))
        if "RF" in self.predict_list:
            if self.r_acc >= max(self.accuracy_list):
                my_header.append('Random Forest: MODEL SELECTED')
            else:
                my_header.append('Random Forest')
            my_accuracy.append('RF Accuracy: ' + str(self.r_acc))
        if "SVM" in self.predict_list:
            if self.s_acc >= max(self.accuracy_list):
                my_header.append('SVM: MODEL SELECTED')
            else:
                my_header.append('SVM')
            my_accuracy.append('SVM Accuracy: ' + str(self.s_acc))
        if "GNB" in self.predict_list:
            if self.g_acc >= max(self.accuracy_list):
                my_header.append('GNB: MODEL SELECTED')
            else:
                my_header.append('GNB')
            my_accuracy.append('GNB Accuracy: ' + str(self.g_acc))
        if "MLP" in self.predict_list:
            if self.mlp_acc >= max(self.accuracy_list):
                my_header.append('MLP: MODEL SELECTED')
            else:
                my_header.append('MLP')
            my_accuracy.append('MLP Accuracy: ' + str(self.mlp_acc))


        my_header.append('Targeted Prediction')
        my_accuracy.append(self.target)
        with open(file_out_name, mode='w') as _file:
            _writer = csv.writer(_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            _writer.writerow(my_header)
            _writer.writerow(my_accuracy)
            for i in range(self.test_len):
                myrow = []
                if "LR" in self.predict_list: myrow.append(self.y_pred_one_hot_l[i])
                if "RF" in self.predict_list: myrow.append(self.y_pred_one_hot_r[i])
                if "SVM" in self.predict_list: myrow.append(self.y_pred_one_hot_s[i])
                if "GNB" in self.predict_list: myrow.append(self.y_pred_one_hot_s[i])
                if "MLP" in self.predict_list: myrow.append(self.y_pred_one_hot_mlp[i])



                myrow.append(self.y_test_list[i])
                _writer.writerow(myrow)

class OneHotPredictorBuilder(object):
    def __init__(self, target,training_test_split_percent):
        if target == None:
            raise Exception("target cannot be none")
        self.target = target
        self.training_test_split_percent = training_test_split_percent
        self.predict_list = []

    def add_predictor(self, predictor):
        self.predict_list.append(predictor)
        return self

    def build(self):
        return OneHotPredictor(self.target,self.predict_list,self.training_test_split_percent)