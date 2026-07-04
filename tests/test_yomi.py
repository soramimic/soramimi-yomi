import soramimi_yomi


def test_basic_yomi():
    assert soramimi_yomi.get_yomi("海は広いな") == "ウミワヒロイナ"


def test_userdic_compound():
    # 素のnaist-jdicでは 夕/焼/小/焼 に分割され「ユーヤキショーショー」になる。
    # 同梱ユーザー辞書(dic/user.csv)で補正されることを確認
    assert soramimi_yomi.get_yomi("夕焼小焼の赤とんぼ") == "ユウヤケコヤケノアカトンボ"


def test_numbers():
    # pyopenjtalk-plus の数字読みが効いていること(kuromojiでは不可能な芸当)
    assert soramimi_yomi.get_yomi("1羽のうさぎ") == "イチワノウサギ"
    assert soramimi_yomi.get_yomi("2020年5月") == "ニセンニジューネンゴガツ"


def test_english_rule():
    # BEP辞書による英語→カナ(素のpyopenjtalkはスペル読みしてしまう)
    yomi = soramimi_yomi.get_yomi("Hello, nice to meet you")
    assert "エヌ" not in yomi  # スペル読みになっていない
    assert yomi.startswith("ハロー")


def test_accent_marks_stripped():
    # NJDのアクセント記号(’)が読みに混入しないこと
    assert "’" not in soramimi_yomi.get_yomi("うさぎ追いしかの山")


def test_tokens_kuromoji_compatible():
    tokens = soramimi_yomi.get_tokens("海は広いな")
    assert tokens[0]["surface_form"] == "海"
    assert tokens[0]["pronunciation"] == "ウミ"
    assert tokens[0]["pos"] == "名詞"
    for key in (
        "surface_form", "basic_form", "reading", "pronunciation",
        "pos", "pos_detail_1", "conjugated_type", "conjugated_form",
        "word_position", "chain_flag",
    ):
        assert key in tokens[0]


def test_tokens_keep_surface():
    # /tokenize は表層を保つ(英語正規化を適用しない)。
    # ただし pyopenjtalk は英字を全角に正規化する点に注意
    tokens = soramimi_yomi.get_tokens("Hello world")
    assert any("Ｈｅｌｌｏ" in t["surface_form"] for t in tokens)
