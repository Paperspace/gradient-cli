import click
import pytest

from gradient.cli.deployments import validate_autoscaling_metric_or_resource


def test_should_return_none_if_none_was_provided():
    rv = validate_autoscaling_metric_or_resource(1, 2, None, "Metric")
    assert rv is None


def test_should_raise_bad_parameter_if_provided_value_was_not_valid():
    with pytest.raises(click.BadParameter):
        validate_autoscaling_metric_or_resource(1, 2, ["cpu"], "Metric")


def test_should_return_valid_structure_if_value_format_was_correct():
    expected_value = (
        {
            "type": "Metric",
            "name": "cpu",
            "value_type": "target",
            "value": 60,
        },
        {
            "type": "Metric",
            "name": "gpu",
            "value_type": "target",
            "value": 40,
        },
    )

    rv = validate_autoscaling_metric_or_resource(1, 2, ["cpu/target:60", "gpu/target:40"], "Metric")

    assert rv == expected_value
