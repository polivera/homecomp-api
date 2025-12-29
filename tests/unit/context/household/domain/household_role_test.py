"""Unit tests for HouseholdRole value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.household.domain.value_objects import HouseholdRole


@pytest.mark.unit
class TestHouseholdRole:
    """Tests for HouseholdRole value object"""

    def test_valid_participant_role_creation(self):
        """Test creating valid participant role"""
        role = HouseholdRole("participant")
        assert role.value == "participant"

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="Role cannot be empty"):
            HouseholdRole("")

    def test_invalid_role_raises_error(self):
        """Test that invalid role raises ValueError"""
        with pytest.raises(
            ValueError, match="Invalid role: 'admin'. Must be one of"
        ):
            HouseholdRole("admin")

    def test_owner_role_raises_error(self):
        """Test that owner role raises ValueError (owner is implicit)"""
        with pytest.raises(ValueError, match="Invalid role: 'owner'. Must be one of"):
            HouseholdRole("owner")

    def test_case_sensitive_role(self):
        """Test that role validation is case sensitive"""
        with pytest.raises(
            ValueError, match="Invalid role: 'Participant'. Must be one of"
        ):
            HouseholdRole("Participant")

    def test_valid_roles_constant(self):
        """Test that VALID_ROLES contains expected roles"""
        assert "participant" in HouseholdRole.VALID_ROLES
        assert len(HouseholdRole.VALID_ROLES) == 1

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # Should work even with invalid role
        role = HouseholdRole.from_trusted_source("invalid_role")
        assert role.value == "invalid_role"

        # Should work even with empty string
        role = HouseholdRole.from_trusted_source("")
        assert role.value == ""

    def test_immutability(self):
        """Test that value object is immutable"""
        role = HouseholdRole("participant")
        with pytest.raises(FrozenInstanceError):
            role.value = "admin"
