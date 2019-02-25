from sklearn import svm, preprocessing
#dummy data
train_x = [[1], [2], [3], [4]]
train_y = [ 0, 0, 1,2]
test_x = [[0], [2.3], [5]]

#training the svm
scaler = preprocessing.StandardScaler().fit(train_x)
train_x_norm = scaler.transform(train_x)
clf = svm.SVC(gamma='scale', decision_function_shape='ovo',kernel='poly')
clf.fit(train_x_norm ,train_y)

#using the svm for classifying unknown objects
test_x_norm = scaler.transform(test_x)
unkw_y = clf.predict(test_x_norm)
print(unkw_y)