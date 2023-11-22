import pytest

from airflow_helper.remote import AirflowAPIGrabber

params_list = [
    ({}, "http://localhost:8080/api/v1"),
    (dict(host="custom-host"), "http://custom-host:8080/api/v1"),
    (dict(host="https://custom-host"), "https://custom-host:8080/api/v1"),
    (dict(host="https://custom-host", port=2020), "https://custom-host:2020/api/v1"),
    (
        dict(url="https://airflow:9090", host="https://custom-host", port=2020),
        "https://airflow:9090/api/v1",
    ),
]


@pytest.mark.parametrize("params,result", params_list)
def test_airflow_uri_default(params, result):
    assert AirflowAPIGrabber.get_airflow_url(**params) == result
