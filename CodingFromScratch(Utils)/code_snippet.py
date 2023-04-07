target_or = target
num_cols = df[features]._get_numeric_data().columns
categorical_cols = set(features)-set(list(num_cols))
one_hot_encoded_data = pd.get_dummies(df[features], columns = list(categorical_cols))

X,y = one_hot_encoded_data,target_or
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=_)
X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
smote_ebm = ExplainableBoostingClassifier(random_state=seed, n_jobs=-1)
smote_ebm.fit(X_resampled, y_resampled) 
smote_train_acc = smote_ebm.score(X_train,y_train)
smote_test_acc = smote_ebm.score(X_test, y_test)
smote_f1 = f1_score(list(y_test),smote_ebm.predict(X_test),average='weighted')
if smote_f1< 0.8 and best_update == False:
  print(f">>early stopping for loop: {smote_f1}")
  break
if smote_f1> best_f1 and smote_f1> 0.8:
  best_f1 = smote_f1
  best_update = True
