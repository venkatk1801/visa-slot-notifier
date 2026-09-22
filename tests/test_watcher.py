from checkers import SlotResult, HttpJsonChecker


def test_slot_result_key():
    r = SlotResult("Chennai", True, dates=["2026-10-01", "2026-10-02"])
    assert r.key() == "Chennai:2026-10-01,2026-10-02"


def test_checker_no_url():
    c = HttpJsonChecker({})
    r = c.check("Chennai")
    assert r.available is False
    assert "no url" in r.detail
