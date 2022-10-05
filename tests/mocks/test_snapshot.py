def foo():
    return "foo"


def test_snapshot(snapshot):
    """snapshotのテスト
    foo()の返り値と'snapshots/sample.txt'の内容が一致するかtestする
    pytest --snapshot-updateと実行すれば、foo()の返り値をsample.txtに更新する
    """
    snapshot.snapshot_dir = "snapshots"  # This line is optional.
    snapshot.assert_match(foo(), "sample.txt")
