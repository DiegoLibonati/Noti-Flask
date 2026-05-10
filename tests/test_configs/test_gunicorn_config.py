import multiprocessing

import pytest

import src.configs.gunicorn_config as gunicorn_config


class TestGunicornConfig:
    @pytest.mark.unit
    def test_bind_is_set(self) -> None:
        assert gunicorn_config.bind is not None
        assert ":" in gunicorn_config.bind

    @pytest.mark.unit
    def test_workers_is_positive_integer(self) -> None:
        assert isinstance(gunicorn_config.workers, int)
        assert gunicorn_config.workers > 0

    @pytest.mark.unit
    def test_workers_formula_uses_cpu_count(self) -> None:
        expected: int = multiprocessing.cpu_count() * 2 + 1
        assert gunicorn_config.workers == expected

    @pytest.mark.unit
    def test_threads_is_positive_integer(self) -> None:
        assert isinstance(gunicorn_config.threads, int)
        assert gunicorn_config.threads > 0

    @pytest.mark.unit
    def test_timeout_is_positive_integer(self) -> None:
        assert isinstance(gunicorn_config.timeout, int)
        assert gunicorn_config.timeout > 0

    @pytest.mark.unit
    def test_graceful_timeout_is_positive_integer(self) -> None:
        assert isinstance(gunicorn_config.graceful_timeout, int)
        assert gunicorn_config.graceful_timeout > 0

    @pytest.mark.unit
    def test_loglevel_is_string(self) -> None:
        assert isinstance(gunicorn_config.loglevel, str)

    @pytest.mark.unit
    def test_proc_name_is_set(self) -> None:
        assert gunicorn_config.proc_name == "noti"

    @pytest.mark.unit
    def test_accesslog_is_stdout(self) -> None:
        assert gunicorn_config.accesslog == "-"

    @pytest.mark.unit
    def test_errorlog_is_stdout(self) -> None:
        assert gunicorn_config.errorlog == "-"
