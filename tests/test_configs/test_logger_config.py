import logging

import pytest

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    @pytest.mark.unit
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger()
        assert isinstance(logger, logging.Logger)

    @pytest.mark.unit
    def test_default_name_is_noti(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "noti"

    @pytest.mark.unit
    def test_custom_name_is_used(self) -> None:
        logger: logging.Logger = setup_logger("my_module")
        assert logger.name == "my_module"

    @pytest.mark.unit
    def test_logger_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger()
        assert len(logger.handlers) >= 1

    @pytest.mark.unit
    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_calling_twice_does_not_add_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("dedup_test")
        handler_count_first: int = len(logger.handlers)
        setup_logger("dedup_test")
        assert len(logger.handlers) == handler_count_first
