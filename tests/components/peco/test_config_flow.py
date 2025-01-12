"""Test the PECO Outage Counter config flow."""
from unittest.mock import patch

from pytest import raises
from voluptuous.error import MultipleInvalid

from homeassistant import config_entries
from homeassistant.components.peco.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import RESULT_TYPE_CREATE_ENTRY, RESULT_TYPE_FORM


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == RESULT_TYPE_FORM
    assert result["errors"] is None

    with patch(
        "homeassistant.components.peco.async_setup_entry",
        return_value=True,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "county": "PHILADELPHIA",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "Philadelphia Outage Count"
    assert result2["data"] == {
        "county": "PHILADELPHIA",
    }


async def test_invalid_county(hass: HomeAssistant) -> None:
    """Test if the InvalidCounty error works."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == RESULT_TYPE_FORM
    assert result["errors"] is None

    with raises(MultipleInvalid):
        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "county": "INVALID_COUNTY_THAT_SHOULD_NOT_EXIST",
            },
        )
        await hass.async_block_till_done()

    # it should have errored, instead of returning an errors dict, since this error should never happen
