from pyspark.ml.feature import VectorAssembler

def get_feature_columns():
    return [
        'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
        'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 
        'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 
        'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
    ]

def assemble_features(df, input_cols=None):
    if input_cols is None:
        input_cols = get_feature_columns()
    available_cols = [col for col in input_cols if col in df.columns]
    assembler = VectorAssembler(inputCols=available_cols, outputCol="features")
    return assembler.transform(df)
