from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from flask.testing import FlaskClient


class TestNoteControllerAlive:
    @pytest.mark.unit
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_alive_returns_expected_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict = response.get_json()
        assert data["message"] == "I am Alive!"
        assert data["name_bp"] == "Notes"


class TestNoteControllerGetAll:
    @pytest.mark.unit
    def test_get_all_returns_200(self, client: FlaskClient) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_get_all_returns_notes_in_data(self, client: FlaskClient) -> None:
        mock_note: MagicMock = MagicMock()
        mock_note.to_dict.return_value = {"id": 1, "content": "test", "user_id": 1, "created_at": "2024-01-01T00:00:00"}
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[mock_note]):
            response = client.get("/api/v1/notes/")
        data: dict = response.get_json()
        assert len(data["data"]) == 1

    @pytest.mark.unit
    def test_get_all_returns_empty_data(self, client: FlaskClient) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        data: dict = response.get_json()
        assert data["data"] == []


class TestNoteControllerCreate:
    @pytest.mark.unit
    def test_create_returns_401_when_not_authenticated(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/notes/", json={"content": "hello"})
        assert response.status_code in (401, 302)

    @pytest.mark.integration
    def test_create_returns_201_when_authenticated(
        self, app: Flask, auth_client: FlaskClient, db_session: None
    ) -> None:
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=MagicMock()):
            response = auth_client.post("/api/v1/notes/", json={"content": "hello"})
        assert response.status_code == 201

    @pytest.mark.integration
    def test_create_returns_redirect_path_in_response(
        self, app: Flask, auth_client: FlaskClient, db_session: None
    ) -> None:
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=MagicMock()):
            response = auth_client.post("/api/v1/notes/", json={"content": "hello"})
        data: dict = response.get_json()
        assert "redirect_to" in data


class TestNoteControllerDelete:
    @pytest.mark.unit
    def test_delete_returns_302_when_not_authenticated(self, client: FlaskClient) -> None:
        response = client.delete("/api/v1/notes/1")
        assert response.status_code in (401, 302)

    @pytest.mark.integration
    def test_delete_returns_200_when_note_found(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        mock_note: MagicMock = MagicMock()
        with patch("src.controllers.note_controller.NoteService.get_note_by_id", return_value=mock_note):
            with patch("src.controllers.note_controller.NoteService.delete_note"):
                response = auth_client.delete("/api/v1/notes/1")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_delete_returns_404_when_note_not_found(
        self, app: Flask, auth_client: FlaskClient, db_session: None
    ) -> None:
        with patch("src.controllers.note_controller.NoteService.get_note_by_id", return_value=None):
            response = auth_client.delete("/api/v1/notes/999")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_delete_returns_400_for_non_integer_id(
        self, app: Flask, auth_client: FlaskClient, db_session: None
    ) -> None:
        response = auth_client.delete("/api/v1/notes/abc")
        assert response.status_code == 400


class TestNoteControllerEdit:
    @pytest.mark.unit
    def test_edit_returns_302_when_not_authenticated(self, client: FlaskClient) -> None:
        response = client.patch("/api/v1/notes/1", json={"content": "updated"})
        assert response.status_code in (401, 302)

    @pytest.mark.integration
    def test_edit_returns_200_when_successful(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        mock_note: MagicMock = MagicMock()
        with patch("src.controllers.note_controller.NoteService.get_note_by_id", return_value=mock_note):
            with patch("src.controllers.note_controller.NoteService.update_note"):
                response = auth_client.patch("/api/v1/notes/1", json={"content": "updated"})
        assert response.status_code == 200

    @pytest.mark.integration
    def test_edit_returns_400_for_non_integer_id(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        response = auth_client.patch("/api/v1/notes/abc", json={"content": "x"})
        assert response.status_code == 400

    @pytest.mark.integration
    def test_edit_returns_400_for_empty_content(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        response = auth_client.patch("/api/v1/notes/1", json={"content": ""})
        assert response.status_code == 400

    @pytest.mark.integration
    def test_edit_returns_404_when_note_not_found(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        with patch("src.controllers.note_controller.NoteService.get_note_by_id", return_value=None):
            response = auth_client.patch("/api/v1/notes/999", json={"content": "new"})
        assert response.status_code == 404
