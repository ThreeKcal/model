from threekcal_model.model import prediction

def test_prediction():
    a="That dog is very cute"
    b = prediction(a) 
    assert isinstance(b,list) 
