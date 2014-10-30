from pavara.network import packet

def test_flatten():
    p = packet.PlayerMovement(1, 666)
    assert len(p.flatten()) == 8
