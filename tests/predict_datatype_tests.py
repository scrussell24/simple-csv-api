from api.predict_datatype import predict_datatype


def test_prediction_datetime_mmddYYYY():
    expected = "DATETIME"
    prediction = predict_datatype("7/4/1776").value
    assert prediction == expected


def test_prediction_datetime_mmddyy():
    expected = "DATETIME"
    prediction = predict_datatype("7/4/76").value
    assert prediction == expected


def test_prediction_number_int():
    expected = "NUMBER"
    prediction = predict_datatype("4").value
    assert prediction == expected


def test_prediction_number_decimal():
    expected = "NUMBER"
    prediction = predict_datatype("4.001").value
    assert prediction == expected


def test_prediction_number_leading_zeroes():
    expected = "NUMBER"
    prediction = predict_datatype("0001.1").value
    assert prediction == expected


def test_prediction_text():
    expected = "TEXT"
    prediction = predict_datatype("anything else").value
    assert prediction == expected
